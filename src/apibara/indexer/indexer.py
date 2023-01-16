import asyncio
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional

from grpc import StatusCode
from grpc.aio import AioRpcError

from apibara.indexer.configuration import Data, Filter, IndexerConfiguration
from apibara.indexer.info import Info, UserContext
from apibara.protocol.proto.stream_pb2 import Cursor


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
    def decode_data(self, raw: bytes) -> Data:
        raise NotImplementedError()

    @abstractmethod
    async def handle_data(self, info: Info[UserContext, Filter], data: Data):
        raise NotImplementedError()

    async def handle_pending_data(self, info: Info[UserContext, Filter], data: Data):
        raise NotImplementedError()

    async def handle_invalidate(self, info: Info[UserContext, Filter], cursor: Cursor):
        return

    async def handle_reconnect(self, exc: Exception, retry_count: int) -> Reconnect:
        if not isinstance(exc, AioRpcError):
            return Reconnect(reconnect=False)

        if exc.code != StatusCode.INTERNAL:
            return Reconnect(reconnect=False)

        await asyncio.sleep(retry_count)
        return Reconnect(reconnect=retry_count < 5)
