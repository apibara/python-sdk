import asyncio
from asyncio.queues import Queue
from typing import AsyncIterable, Iterable, Optional, Tuple, Union

import grpc
from grpc.aio import Channel

from apibara.protocol.proto.stream_pb2 import (Cursor, DataFinality,
                                               StreamDataRequest,
                                               StreamDataResponse)
from apibara.protocol.proto.stream_pb2_grpc import StreamStub

DEFAULT_TIMEOUT = 45.0


class BearerTokenAuth(grpc.AuthMetadataPlugin):
    def __init__(self, token: str):
        if token is not None:
            self._meta = [("authorization", f"bearer {token}")]
        else:
            self._meta = []

    def __call__(self, context, callback):
        callback(self._meta, None)


def credentials_with_auth_token(token: str, credentials: grpc.CallCredentials):
    """Returns new credentials that authenticate with the server."""
    return grpc.composite_channel_credentials(
        credentials, grpc.metadata_call_credentials(BearerTokenAuth(token))
    )


class StreamService:
    """
    An Apibara Stream service.

    Arguments
    ---------
    channel: grpc.aio.Channel
        the grpc channel
    token: str, optional
        authentication token sent to the server
    """

    def __init__(self, channel: Channel) -> None:
        self._channel = channel
        self._stub = StreamStub(self._channel)

    def stream_data(self, timeout=None) -> Tuple["StreamClient", "StreamIter"]:
        """Start streaming data from the server.

        Arguments
        ---------
        timeout: float
            timeout in seconds for waiting messages from the server.
        """
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        ctx = _Context()
        client = StreamClient(ctx)
        iter = self._stub.StreamData(client.client_stream)
        stream = StreamIter(ctx, iter, timeout)
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
        cursor: Optional[Cursor] = None,
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
    def __init__(
        self, ctx: "_Context", inner: grpc.StreamStreamMultiCallable, timeout: float
    ) -> None:
        self._ctx = ctx
        self._inner = inner
        self._timeout = timeout
        self._iter = None

    def __aiter__(self) -> AsyncIterable[StreamDataResponse]:
        self._iter = self._inner.__aiter__()
        return self

    async def __anext__(self):
        while True:
            value = await asyncio.wait_for(
                self._iter.__anext__(), timeout=self._timeout
            )
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
