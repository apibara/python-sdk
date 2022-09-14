"""Apibara indexer runner."""

import base64
import warnings
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, List, Optional, TypeVar

from grpc.aio import AioRpcError
from grpc_requests.aio import AsyncClient
from starknet_py.contract import ContractFunction

from apibara.indexer.storage import IndexerStorage, Storage
from apibara.logging import logger
from apibara.model import (
    BlockHeader,
    EventFilter,
    NewBlock,
    NewEvents,
    Reorg,
    StarkNetEvent,
)

UserContext = TypeVar("UserContext")


@dataclass
class Info(Generic[UserContext]):
    context: UserContext
    storage: Storage


NewEventsHandler = Callable[[Info, NewEvents], Awaitable[None]]
BlockHandler = Callable[[Info, NewBlock], Awaitable[None]]
ReorgHandler = Callable[[Info, Reorg], Awaitable[None]]


@dataclass
class IndexerRunnerConfiguration:
    apibara_url: Optional[str] = None
    apibara_ssl: bool = False
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
        reset_state: bool = False,
        config: Optional[IndexerRunnerConfiguration] = None,
    ) -> None:
        if config is None:
            config = IndexerRunnerConfiguration()
        self._reset_state = reset_state
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
        # self._rpc_client = StarkNetRpcClient(self._config.rpc_url)

        self._indexer_config = None
        self._compiled_filters = None
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
        self._print_deprecation_notice()
        self._check_config()
        if self._reset_state:
            self._delete_old_state()
        await self._do_run()

    def _check_config(self):
        if self._config is None:
            raise RuntimeError("must provide config to IndexerRunner")

        if self._config.apibara_url is None:
            raise RuntimeError("must provide an apibara_url in config")

        if self._config.storage_url is None:
            raise RuntimeError("must provide a storage_url in config")

    def _print_deprecation_notice(self):
        warnings.warn(
            "IndexerRunner is deprecated and will be removed in the next release.",
            DeprecationWarning,
        )

    def _delete_old_state(self):
        self._indexer_storage.drop_database()

    async def _do_run(self):
        # Try to start from where the previous run left off
        starting_sequence = self._indexer_storage.starting_sequence()
        if starting_sequence is None:
            starting_sequence = self._indexer_config["index_from_block"]

        client = AsyncClient(self._config.apibara_url, ssl=self._config.apibara_ssl)

        node_service = await client.service("apibara.node.v1alpha1.Node")

        self._compile_event_filters()

        async for message in await node_service.Connect(
            {"starting_sequence": starting_sequence}
        ):
            if "data" in message:
                block = message["data"]["data"]
                block_header = BlockHeader.from_proto(block)
                events = self._block_events_matching_filters(block)
                new_events = NewEvents(block=block_header, events=events)

                with self._block_context(block_header.number) as info:
                    if new_events.events:
                        await self._new_events_handler(info, new_events)

            elif "invalidate" in message:
                raise RuntimeError("reorg are not expected on StarkNet")

    @contextmanager
    def _block_context(self, number: int) -> Info[UserContext]:
        with self._indexer_storage.create_storage_for_block(number) as storage:
            yield Info(context=self._context, storage=storage)

    def _compile_event_filters(self):
        self._compiled_filters = [
            CompiledEventFilter.from_event_filter(filter)
            for filter in self._indexer_config["filters"]
        ]

    def _block_events_matching_filters(self, block):
        matched_events = []
        log_index = 0
        transactions = block["transactions"]
        for receipt in block["transaction_receipts"]:
            # tx = transactions[receipt.get("transaction_index", 0)]
            if "events" in receipt:
                for event in receipt["events"]:
                    event_name, matched = self._filter_matching(event)
                    if matched:
                        event = StarkNetEvent.from_proto(event, log_index, event_name)
                        matched_events.append(event)
                    log_index += 1
        return matched_events

    def _filter_matching(self, event):
        for filter in self._compiled_filters:
            if filter.matches(event):
                return filter.name, True
        return None, False


@dataclass
class CompiledEventFilter:
    name: str
    keys: List[bytes]
    address: Optional[bytes]

    @classmethod
    def from_event_filter(cls, filter: EventFilter):
        return CompiledEventFilter(
            name=filter.signature,
            keys=[ContractFunction.get_selector(filter.signature).to_bytes(32, "big")],
            address=filter.address.ljust(32, b"\0"),
        )

    def matches(self, event):
        if "keys" not in event:
            return False

        if self.address is not None and "from_address" in event:
            event_address = base64.b64decode(event["from_address"]).ljust(32, b"\0")
            if event_address != self.address:
                return False

        event_keys = [base64.b64decode(k).ljust(32, b"\0") for k in event["keys"]]

        return event_keys == self.keys
