from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from apibara.indexer.storage import Filter, Storage
from apibara.protocol.proto.stream_pb2 import Cursor

UserContext = TypeVar("UserContext")


@dataclass
class Info(Generic[UserContext, Filter]):
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
    cursor: Cursor
    end_cursor: Cursor

    _new_filter: Optional[Filter] = None

    def merge_filter(self, filter: Filter):
        """Add the new filter by merging it with the old filter.

        The indexer will re-scan the current block for any data
        matching the new filter.
        """
        self._new_filter = filter

    def _take_new_filter(self):
        """Returns the new filter, if set by the caller."""
        filter = self._new_filter
        self._new_filter = None
        return filter
