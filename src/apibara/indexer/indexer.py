import asyncio
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from apibara.indexer.info import Info, UserContext
from apibara.protocol.proto.stream_pb2 import Cursor, DataFinality

Data = TypeVar("Data")
Filter = TypeVar("Filter")


@dataclass
class IndexerConfiguration(Generic[Filter]):
    filter: Filter
    starting_cursor: Optional[Cursor] = None
    finality: Optional[DataFinality.ValueType] = None


@dataclass
class Reconnect:
    """
    Reconnect configuration.

    Parameters
    ----------
    reconnect: bool
        reconnect to the stream
    cursor: Cursor
        reconnect from this cursor
    """

    reconnect: bool
    cursor: Optional[Cursor] = None


class Indexer(Generic[Filter, Data], metaclass=ABCMeta):
    @abstractmethod
    def indexer_id(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def initial_configuration(self) -> IndexerConfiguration[Filter]:
        raise NotImplementedError()

    @abstractmethod
    def encode_filter(self, filter: Filter) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def parse_data(self, raw: bytes) -> Data:
        raise NotImplementedError()

    @abstractmethod
    async def handle_data(self, info: Info[UserContext, Filter], data: Data):
        raise NotImplementedError()

    async def handle_invalidate(self, info: Info[UserContext, Filter], cursor: Cursor):
        return

    async def handle_reconnect(self, exc: Exception, retry_count: int) -> Reconnect:
        await asyncio.sleep(retry_count)
        return Reconnect(reconnect=retry_count < 5)
