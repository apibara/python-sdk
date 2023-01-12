from asyncio.queues import Queue
from typing import AsyncIterable, Iterable, Optional, Tuple, Union

from grpc import StreamStreamMultiCallable
from grpc.aio import Channel

from apibara.protocol.proto.stream_pb2 import (Cursor, DataFinality,
                                               StreamDataRequest,
                                               StreamDataResponse)
from apibara.protocol.proto.stream_pb2_grpc import StreamStub


class StreamService:
    """
    An Apibara Stream service.

    Arguments
    ---------
    channel: grpc.aio.Channel
        the grpc channel
    """

    def __init__(self, channel: Channel) -> None:
        self._channel = channel
        self._stub = StreamStub(self._channel)

    def stream_data(self) -> Tuple["StreamClient", "StreamIter"]:
        ch = _RequestChannel()
        iter = self._stub.StreamData(ch)
        client = StreamClient(ch)
        stream = StreamIter(iter)
        return client, stream


class StreamClient:
    def __init__(self, ch: "_RequestChannel") -> None:
        self._ch = ch
        self._stream_id = 0

    async def configure(
        self,
        *,
        filter: Optional[bytes] = None,
        batch_size: Optional[int] = None,
        finality: Optional[DataFinality.ValueType] = None,
        cursor: Optional[Cursor] = None
    ):
        self._stream_id += 1
        request = StreamDataRequest(
            stream_id=self._stream_id,
            filter=filter,
            starting_cursor=cursor,
            batch_size=batch_size,
            finality=finality,
        )
        await self._ch.push(request)


class StreamIter:
    def __init__(self, inner: StreamStreamMultiCallable) -> None:
        self._inner = inner

    def __aiter__(self) -> AsyncIterable[StreamDataResponse]:
        return self._inner.__aiter__()


class _RequestChannel:
    def __init__(self) -> None:
        self._q = Queue(maxsize=32)

    async def push(self, request: StreamDataRequest):
        await self._q.put(request)

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self._q.get()
