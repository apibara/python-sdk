from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Generic, List, Optional, TypeVar

from apibara.indexer.events import EventMatcher
from apibara.indexer.storage import IndexerStorage, Storage
from apibara.model import BlockHeader, EventFilter, NewBlock, NewEvents, Reorg

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

    def _take_new_matcher(self):
        """Returns the new EventMatcher for the next loop."""
        filters = self._new_event_filters
        self._new_event_filters = []
        if filters:
            return EventMatcher(filters)
        return None


NewEventsHandler = Callable[[Info, NewEvents], Awaitable[None]]
BlockHandler = Callable[[Info, NewBlock], Awaitable[None]]
ReorgHandler = Callable[[Info, int], Awaitable[None]]


class MessageHandler:
    """Class used to handle stream messages."""

    def __init__(
        self,
        *,
        data_handler: NewEventsHandler,
        block_handler: Optional[BlockHandler],
        reorg_handler: Optional[ReorgHandler],
        pending_handler: Optional[NewEventsHandler],
        context: UserContext,
        storage: IndexerStorage,
        starting_filters: List[EventFilter]
    ) -> None:
        self._data_handler = data_handler
        self._block_handler = block_handler
        self._reorg_handler = reorg_handler
        self._pending_handler = pending_handler
        self._context = context
        self._storage = storage
        self._has_received_pending_block = False
        self._matcher = EventMatcher(starting_filters)

    async def handle_data(self, block: Any):
        """Handle a `block` message, calling the user-defined handler."""
        block_header = BlockHeader.from_proto(block)

        # invalidate any data stored from a pending block.
        if self._has_received_pending_block:
            self._storage.invalidate(block_header.number)

        with self._data_context(block_header.number) as info:
            if self._block_handler:
                new_block = NewBlock(new_head=block_header)
                await self._block_handler(info, new_block)

            final_matcher = None
            loop_matcher = self._matcher
            while loop_matcher is not None:
                events = loop_matcher.find_events_in_block(block)
                new_events = NewEvents(block=block_header, events=events)

                if new_events.events:
                    await self._data_handler(info, new_events)

                # check if handling this block created new dynamic filters.
                # if that's the case, store the new matcher in `loop_matcher`
                # for use in the next loop.
                # also update `final_matcher`: if is None then no change happened
                # and there is no need to update it at the end of the loop.
                # if it changed, then update it.
                new_matcher = info._take_new_matcher()
                if new_matcher:
                    if final_matcher is None:
                        final_matcher = self._matcher
                    final_matcher = final_matcher.merge(new_matcher)
                    loop_matcher = new_matcher
                else:
                    loop_matcher = None

            if final_matcher is not None:
                self._matcher = final_matcher
                new_filters = final_matcher._filters
                self._storage._set_event_filters(
                    new_filters, session=info.storage._session
                )

    async def handle_invalidate(self, invalidate: Any):
        """Handle an `invalidate` message, rolling back the storage state."""
        sequence = invalidate["sequence"]
        self._storage.invalidate(sequence)
        if self._reorg_handler:
            with self._invalidate_context(sequence) as info:
                await self._reorg_handler(info, sequence)

    async def handle_pending(self, block: Any):
        """Handle a `pending` message, calling the user-defined handler, if any."""
        if self._pending_handler is None:
            return

        block_header = BlockHeader.from_proto(block)
        events = self._matcher.find_events_in_block(block)
        new_events = NewEvents(block=block_header, events=events)

        # invalidate previous pending data
        if self._has_received_pending_block:
            self._storage.invalidate(block_header.number)

        # no event matching. nothing to do here
        if not new_events.events:
            return

        with self._pending_context(block_header.number) as info:
            self._has_received_pending_block = True
            await self._pending_handler(info, new_events)
            if info._take_new_matcher():
                raise RuntimeError(
                    "cannot create dynamic filters in pending data handler"
                )

    @contextmanager
    def _data_context(self, number: int) -> Info[UserContext]:
        with self._storage.create_storage_for_data(number) as storage:
            yield Info(context=self._context, storage=storage)

    @contextmanager
    def _invalidate_context(self, number: int) -> Info[UserContext]:
        with self._storage.create_storage_for_invalidate(number) as storage:
            yield Info(context=self._context, storage=storage)

    @contextmanager
    def _pending_context(self, number: int) -> Info[UserContext]:
        with self._storage.create_storage_for_pending(number) as storage:
            yield Info(context=self._context, storage=storage)
