"""Apibara indexer runner."""

from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, List, Optional, TypeVar

import backoff
from grpc.aio import AioRpcError

from apibara.client import Client
from apibara.indexer.indexer import IndexerClient
from apibara.logging import logger
from apibara.model import EventFilter, Indexer, NewBlock, NewEvents, Reorg
from apibara.rpc import RpcClient
from apibara.starknet import get_selector_from_name
from apibara.starknet.rpc import StarkNetRpcClient

UserContext = TypeVar("UserContext")


@dataclass
class Info(Generic[UserContext]):
    context: UserContext
    rpc_client: RpcClient


NewEventsHandler = Callable[[Info, NewEvents], Awaitable[None]]
BlockHandler = Callable[[Info, NewBlock], Awaitable[None]]
ReorgHandler = Callable[[Info, Reorg], Awaitable[None]]


@dataclass
class IndexerRunnerConfiguration:
    apibara_url: Optional[str] = None
    rpc_url: Optional[str] = None


class IndexerRunner(Generic[UserContext]):
    """Run an indexer, listening for new events and calling the provided callbacks."""

    def __init__(
        self,
        *,
        indexer_id: str,
        new_events_handler: NewEventsHandler,
        config: Optional[IndexerRunnerConfiguration] = None,
    ) -> None:
        if config is None:
            config = IndexerRunnerConfiguration()
        self._indexer_id = indexer_id
        self._config = config
        self._new_events_handler = new_events_handler
        self._block_handler = None
        self._reorg_handler = None
        self._context = None

        self._indexer_config = None
        self._event_topic_to_name_map = None

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

            self._initialize_event_topic_map()

            await self._run_indexer(indexer_client, indexer)

    async def _run_indexer(self, client: IndexerClient, indexer: Indexer):
        info = self._create_info()
        async with client.connect(indexer) as stream:
            async for message in stream:
                if isinstance(message, NewBlock):
                    await self._handle_new_block(info, message)
                elif isinstance(message, Reorg):
                    await self._handle_reorg(info, message)
                elif isinstance(message, NewEvents):
                    await self._handle_new_events(info, message)
                    # inform server that events were handled
                    await stream.ack_block(message.block_hash)
                    logger.debug(f"Acked block 0x{message.block_hash.hex()}")
                else:
                    raise RuntimeError(f"Unknown message: {message}")

    async def _handle_new_block(self, info: Info[UserContext], message: NewBlock):
        if self._block_handler is None:
            return
        await self._block_handler(info, message)

    async def _handle_reorg(self, info: Info[UserContext], message: Reorg):
        if self._reorg_handler is None:
            return
        await self._reorg_handler(info, message)

    async def _handle_new_events(self, info: Info[UserContext], message: NewEvents):
        assert self._new_events_handler is not None
        # Add event name to events
        for event in message.events:
            if len(event.topics) == 1:
                topic = event.topics[0].lstrip(b"\x00")
                name = self._event_topic_to_name_map.get(topic)
                event.name = name
        await self._new_events_handler(info, message)

    def _create_info(self) -> Info[UserContext]:
        # TODO: create RpcClient based on the apibara's network.
        rpc_client = StarkNetRpcClient("https://starknet-goerli.apibara.com")
        return Info(context=self._context, rpc_client=rpc_client)

    async def _maybe_create_indexer(self, indexer_client: IndexerClient) -> Indexer:
        if self._indexer_config is None:
            raise RuntimeError(f"Indexer {self._indexer_id} does not exist")
        index_from_block = self._indexer_config["index_from_block"]
        filters = self._indexer_config["filters"]
        indexer = await indexer_client.create_indexer(
            self._indexer_id, index_from_block, filters
        )
        logger.debug("Created new indexer")
        return indexer

    def _initialize_event_topic_map(self):
        self._event_topic_to_name_map = dict()
        if self._indexer_config is None:
            return
        filters = self._indexer_config["filters"]
        if filters is None:
            return

        result = dict()
        for filter in filters:
            if filter.name is None:
                continue
            topic_hex = hex(get_selector_from_name(filter.name))[2:]
            # fromhex requires an even number of digits
            if len(topic_hex) % 2 == 1:
                topic_hex = "0" + topic_hex
            topic_value = bytes.fromhex(topic_hex).lstrip(b"\x00")
            result[topic_value] = filter.name

        self._event_topic_to_name_map = result
