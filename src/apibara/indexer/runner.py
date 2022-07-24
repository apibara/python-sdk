"""Apibara indexer runner."""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, List, Optional, TypeVar

import backoff
import sha3
from grpc.aio import AioRpcError

from apibara.client import Client
from apibara.indexer.indexer import IndexerClient
from apibara.indexer.storage import IndexerStorage, Storage
from apibara.logging import logger
from apibara.model import (
    EthereumEvent,
    Event,
    EventFilter,
    Indexer,
    NewBlock,
    NewEvents,
    Reorg,
    StarkNetEvent,
)
from apibara.rpc import RpcClient
from apibara.starknet import get_selector_from_name
from apibara.starknet.rpc import StarkNetRpcClient

UserContext = TypeVar("UserContext")


@dataclass
class Info(Generic[UserContext]):
    context: UserContext
    rpc_client: RpcClient
    storage: Storage


NewEventsHandler = Callable[[Info, NewEvents], Awaitable[None]]
BlockHandler = Callable[[Info, NewBlock], Awaitable[None]]
ReorgHandler = Callable[[Info, Reorg], Awaitable[None]]


@dataclass
class IndexerRunnerConfiguration:
    apibara_url: Optional[str] = None
    rpc_url: Optional[str] = None
    storage_url: Optional[str] = None


class IndexerRunner(Generic[UserContext]):
    """Run an indexer, listening for new events and calling the provided callbacks."""

    def __init__(
        self,
        *,
        indexer_id: str,
        network_name: str,
        new_events_handler: NewEventsHandler,
        config: Optional[IndexerRunnerConfiguration] = None,
    ) -> None:
        if config is None:
            config = IndexerRunnerConfiguration()
        self._indexer_id = indexer_id
        self._network_name = network_name
        self._config = config
        self._new_events_handler = new_events_handler
        self._block_handler = None
        self._reorg_handler = None
        self._context = None
        self._indexer_storage = IndexerStorage(
            self._config.storage_url, self._indexer_id
        )
        self._rpc_client = StarkNetRpcClient(self._config.rpc_url)

        self._indexer_config = None
        self._event_name_map = dict()

    def create_if_not_exists(
        self,
        filters: Optional[List[EventFilter]] = None,
        index_from_block: Optional[int] = None,
    ):
        """If the indexer does not exist on the server, create it."""
        self._indexer_config = {
            "filters": filters,
            "index_from_block": index_from_block,
        }

    def set_context(self, context: UserContext):
        """Set the context object used to share information between handlers."""
        self._context = context

    def add_block_handler(self, block_handler: BlockHandler) -> None:
        """Add a callback called every time there is a new block."""
        self._block_handler = block_handler

    def add_reorg_handler(self, reorg_handler: ReorgHandler) -> None:
        """Add a callback called every time there is a chain reorganization."""
        self._reorg_handler = reorg_handler

    async def run(self):
        """Run the indexer until stopped."""
        # Call the helper function that will retry in case of GrpError,
        # like for example on disconnect.
        await self._do_run()

    @backoff.on_exception(backoff.expo, AioRpcError, logger=logger)
    async def _do_run(self):
        async with Client.connect(self._config.apibara_url) as client:
            logger.debug("connected to apibara server")
            indexer_client = client.indexer_client()
            existing = await indexer_client.get_indexer(self._indexer_id)
            if existing is None:
                indexer = await self._maybe_create_indexer(indexer_client)
            else:
                indexer = existing

            await self._run_indexer(indexer_client, indexer)

    async def _run_indexer(self, client: IndexerClient, indexer: Indexer):
        self._create_event_map(indexer)
        async with client.connect(indexer) as stream:
            async for message in stream:
                if isinstance(message, NewBlock):
                    await self._handle_new_block(message)
                elif isinstance(message, Reorg):
                    await self._handle_reorg(message)
                elif isinstance(message, NewEvents):
                    await self._handle_new_events(message)
                    # inform server that events were handled
                    await stream.ack_block(message.block.hash)
                    logger.debug(f"Acked block 0x{message.block.hash.hex()}")
                else:
                    raise RuntimeError(f"Unknown message: {message}")

    @contextmanager
    def _block_context(self, number: int) -> Info[UserContext]:
        with self._indexer_storage.create_storage_for_block(number) as storage:
            yield Info(
                context=self._context, rpc_client=self._rpc_client, storage=storage
            )

    async def _handle_new_block(self, message: NewBlock):
        if self._block_handler is None:
            return
        with self._block_context(message.new_head.number) as info:
            await self._block_handler(info, message)

    async def _handle_reorg(self, message: Reorg):
        if self._reorg_handler is None:
            return
        # TODO: invalidate old data. Before or after user's callback?
        # Why not two callbacks?
        with self._block_context(message.new_head.number) as info:
            await self._reorg_handler(info, message)

    async def _handle_new_events(self, message: NewEvents):
        assert self._new_events_handler is not None
        for event in message.events:
            event.name = self._get_event_name(event)
        with self._block_context(message.block.number) as info:
            await self._new_events_handler(info, message)

    async def _maybe_create_indexer(self, indexer_client: IndexerClient) -> Indexer:
        if self._indexer_config is None:
            raise RuntimeError(f"Indexer {self._indexer_id} does not exist")
        index_from_block = self._indexer_config["index_from_block"]
        filters = self._indexer_config["filters"]
        indexer = await indexer_client.create_indexer(
            self._indexer_id, self._network_name, index_from_block, filters
        )
        logger.debug("Created new indexer")
        return indexer

    def _create_event_map(self, indexer: Indexer):
        if indexer.network.type == "evm":
            return self._create_evm_event_map()
        elif indexer.network.type == "starknet":
            return self._create_starknet_event_map()

    def _create_evm_event_map(self):
        for filter in self._indexer_config["filters"]:
            signature_hash = sha3.keccak_256(filter.signature.encode("ascii")).digest()
            self._event_name_map[signature_hash] = filter.signature

    def _create_starknet_event_map(self):
        for filter in self._indexer_config["filters"]:
            signature_hash = get_selector_from_name(filter.signature)
            self._event_name_map[signature_hash] = filter.signature

    def _get_event_name(self, event: Event):
        if isinstance(event, StarkNetEvent):
            hash = int.from_bytes(event.topics[0], "big")
            return self._event_name_map.get(hash)
        else:
            return self._event_name_map.get(event.topics[0])
