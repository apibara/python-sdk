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
        ctx = _Context()
        client = StreamClient(ctx)
        iter = self._stub.StreamData(client.client_stream)
        stream = StreamIter(ctx, iter)
        return client, stream


class StreamClient:
    def __init__(self, ctx: "_Context") -> None:
        self._ctx = ctx
        self.client_stream = _RequestChannel()

    async def configure(
        self,
        *,
        filter: Optional[bytes] = None,
        batch_size: Optional[int] = None,
        finality: Optional[DataFinality.ValueType] = None,
        cursor: Optional[Cursor] = None
    ):
        self._ctx.stream_id += 1
        request = StreamDataRequest(
            stream_id=self._ctx.stream_id,
            filter=filter,
            starting_cursor=cursor,
            batch_size=batch_size,
            finality=finality,
        )
        await self.client_stream.push(request)


class StreamIter:
    def __init__(self, ctx: "_Context", inner: StreamStreamMultiCallable) -> None:
        self._ctx = ctx
        self._inner = inner
        self._iter = None

    def __aiter__(self) -> AsyncIterable[StreamDataResponse]:
        self._iter = self._inner.__aiter__()
        return self

    async def __anext__(self):
        while True:
            value = await self._iter.__anext__()
            if value.stream_id == self._ctx.stream_id:
                return value


class _Context:
    def __init__(self):
        self.stream_id = 0


class _RequestChannel:
    def __init__(self) -> None:
        self._q = Queue(maxsize=32)

    async def push(self, request: StreamDataRequest):
        await self._q.put(request)

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self._q.get()
