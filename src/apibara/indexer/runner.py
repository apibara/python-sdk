"""Apibara indexer runner."""

import base64
import warnings
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Generic, List, Optional, TypeVar

from grpc.aio import AioRpcError
from grpc_requests.aio import AsyncClient
from starknet_py.contract import ContractFunction

from apibara.indexer.storage import IndexerStorage, Storage
from apibara.logging import logger
from apibara.model import (BlockHeader, EventFilter, NewBlock, NewEvents,
                           Reorg, StarkNetEvent)

UserContext = TypeVar("UserContext")


@dataclass
class Info(Generic[UserContext]):
    """State shared between handlers.
    
    Parameters
    ----------
    context:
        application-specific context.
    storage:
        access the chain-aware storage.
    """
    context: UserContext
    storage: Storage

    _new_event_filters: List[EventFilter] = field(default_factory=list)

    def add_event_filters(self, filters: List[EventFilter]):
        """Add the provided event filters to the indexer.

        The indexer will re-scan the current block for any event
        matching the new filters.
        """
        self._new_event_filters.extend(filters)

    def _take_new_event_filters(self):
        """Returns and empties the current EventFilter list."""
        filters = self._new_event_filters
        self._new_event_filters = []
        return filters


NewEventsHandler = Callable[[Info, NewEvents], Awaitable[None]]
BlockHandler = Callable[[Info, NewBlock], Awaitable[None]]
ReorgHandler = Callable[[Info, Reorg], Awaitable[None]]


@dataclass
class IndexerRunnerConfiguration:
    """IndexerRunner configuration.
    
    Parameters
    ----------
    apibara_url:
        url of the Apibara stream.
    apibara_ssl:
        flag to connect using SSL.
    storage_url:
        MongoDB connection string, used to store the indexer  data and state.
    """
    apibara_url: Optional[str] = None
    apibara_ssl: bool = True
    rpc_url: Optional[str] = None
    storage_url: Optional[str] = None


class IndexerRunner(Generic[UserContext]):
    """Run an indexer, listening for new events and calling the provided callbacks.
    
    Parameters
    ----------
    indexer_id:
        unique id of this indexer. Used when persisting state.
    new_events_handler:
        async function called for each new block containing indexed events.
    reset_state:
        flag to restart the indexer from the beginning.
    config:
        options to set the input stream and connection string.
    """

    def __init__(
        self,
        *,
        indexer_id: str,
        new_events_handler: NewEventsHandler,
        reset_state: bool = False,
        config: Optional[IndexerRunnerConfiguration] = None,
    ) -> None:
        if config is None:
            config = IndexerRunnerConfiguration()
        self._reset_state = reset_state
        self._indexer_id = indexer_id
        self._config = config
        self._new_events_handler = new_events_handler
        self._block_handler = None
        self._reorg_handler = None
        self._context = None
        self._indexer_storage = IndexerStorage(
            self._config.storage_url, self._indexer_id
        )

        self._indexer_config = None
        self._event_name_map = dict()

    def create_if_not_exists(
        self,
        filters: Optional[List[EventFilter]] = None,
        index_from_block: Optional[int] = None,
    ):
        self.add_event_filters(filters, index_from_block)

    def add_event_filters(
        self,
        filters: Optional[List[EventFilter]] = None,
        index_from_block: Optional[int] = None,
    ):
        """Add the initial event filters.
        
        Parameters
        ----------
        filters:
            a list of EventFilter
        index_from_block:
            start indexing from the given block.
        """
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
        self._write_initial_state()
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

    def _write_initial_state(self):
        self._indexer_storage.initialize(
            self._indexer_config["index_from_block"], self._indexer_config["filters"]
        )

    async def _do_run(self):
        client = AsyncClient(self._config.apibara_url, ssl=self._config.apibara_ssl)

        node_service = await client.service("apibara.node.v1alpha1.Node")
        starting_sequence = self._indexer_storage.starting_sequence()
        filters_def = self._indexer_storage.event_filters()
        filters = [CompiledEventFilter.from_event_filter(f) for f in filters_def]

        async for message in await node_service.StreamMessages(
            {"starting_sequence": starting_sequence}
        ):
            if "data" in message:
                block = message["data"]["data"]
                block_header = BlockHeader.from_proto(block)
                with self._block_context(block_header.number) as info:
                    # new filters added across all loops of this block
                    new_filters = []
                    # filters for this specific loop
                    loop_filters = filters
                    while loop_filters:
                        events = self._block_events_matching_filters(
                            loop_filters, block
                        )
                        new_events = NewEvents(block=block_header, events=events)

                        if self._block_handler:
                            new_block = NewBlock(new_head=block_header)
                            await self._block_handler(info, new_block)
                        if new_events.events:
                            await self._new_events_handler(info, new_events)

                        if info._new_event_filters:
                            new_loop_filters = info._take_new_event_filters()
                            new_filters.extend(new_loop_filters)

                            loop_filters = [
                                CompiledEventFilter.from_event_filter(f)
                                for f in new_loop_filters
                            ]
                        else:
                            loop_filters = False

                    # finished parsing events. update state with the new filters
                    if new_filters:
                        filters_def.extend(new_filters)
                        filters_def = _unique_event_filters(filters_def)
                        self._indexer_storage._set_event_filters(
                            filters_def, session=info.storage._session
                        )
                        filters = [
                            CompiledEventFilter.from_event_filter(f)
                            for f in filters_def
                        ]

            elif "invalidate" in message:
                raise RuntimeError("reorg are not expected on StarkNet")

    @contextmanager
    def _block_context(self, number: int) -> Info[UserContext]:
        with self._indexer_storage.create_storage_for_block(number) as storage:
            yield Info(context=self._context, storage=storage)

    def _block_events_matching_filters(self, filters, block):
        matched_events = []
        log_index = 0
        transactions = block.get("transactions", [])
        for receipt in block.get("transaction_receipts",[]):
            tx = transactions[int(receipt.get("transaction_index", 0))]
            if "events" in receipt:
                for event in receipt["events"]:
                    event_name, matched = self._filter_matching(filters, event)
                    if matched:
                        tx_hash = _transaction_hash(tx)
                        event = StarkNetEvent.from_proto(
                            event, log_index, event_name, tx_hash
                        )
                        matched_events.append(event)
                    log_index += 1
        return matched_events

    def _filter_matching(self, filters, event):
        for filter in filters:
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
        address = None
        if filter.address is not None:
            address = filter.address.ljust(32, b"\0")

        return CompiledEventFilter(
            name=filter.signature,
            keys=[ContractFunction.get_selector(filter.signature).to_bytes(32, "big")],
            address=address,
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


def _transaction_hash(tx) -> bytes:
    common = None
    if "invoke" in tx:
        common = tx["invoke"]["common"]
    elif "deploy" in tx:
        common = tx["deploy"]["common"]
    elif "declare" in tx:
        common = tx["declare"]["common"]
    elif "l1_handler" in tx:
        common = tx["l1_handler"]["common"]
    else:
        raise RuntimeError("unknown transaction type")
    return base64.b64decode(common["hash"])


def _unique_event_filters(filters: List[EventFilter]) -> List[EventFilter]:
    return list(set(filters))
