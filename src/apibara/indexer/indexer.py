"""Manage Apibara indexers."""

from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, List, Optional

from aiochannel import Channel
from grpc import StatusCode
from grpc.aio import AioRpcError

import apibara.application.indexer_service_pb2 as indexer_service_pb2
import apibara.application.indexer_service_pb2_grpc as indexer_service_pb2_grpc
from apibara.model import (EventFilter, Indexer, IndexerConnected, NewBlock,
                           NewEvents, Reorg)


class IndexerClient:
    def __init__(self, channel: Channel) -> None:
        self._channel = channel
        self._stub = indexer_service_pb2_grpc.IndexerManagerStub(self._channel)

    async def get_indexer(self, id) -> Optional[Indexer]:
        try:
            response = await self._stub.GetIndexer(
                indexer_service_pb2.GetIndexerRequest(id=id)
            )
            if response and response.indexer and response.indexer.id:
                return Indexer.from_proto(response.indexer)
        except AioRpcError as ex:
            if ex.code() == StatusCode.NOT_FOUND:
                return None
            raise

    async def create_indexer(
        self, id: str, index_from_block: int, filters: List[EventFilter]
    ) -> Optional[Indexer]:
        filters = [f.to_proto() for f in filters]
        response = await self._stub.CreateIndexer(
            indexer_service_pb2.CreateIndexerRequest(
                id=id, index_from_block=index_from_block, filters=filters
            )
        )

        if response and response.indexer:
            return Indexer.from_proto(response.indexer)

    async def delete_indexer(self, id: str) -> Optional[Indexer]:
        response = await self._stub.DeleteIndexer(
            indexer_service_pb2.DeleteIndexerRequest(id=id)
        )

        if response and response.indexer:
            return Indexer.from_proto(response.indexer)

    async def list_indexer(self) -> List[Indexer]:
        response = await self._stub.ListIndexer(
            indexer_service_pb2.ListIndexerRequest()
        )

        return [Indexer.from_proto(ix) for ix in response.indexers]

    @asynccontextmanager
    async def connect(self, indexer: Indexer) -> AsyncIterator["IndexerStream"]:
        # Create indexer stream. Channel is used to send messages
        # to the server.
        channel = Channel()
        response_iter = self._stub.ConnectIndexer(channel)
        stream = IndexerStream(channel, response_iter)

        # Connect and await for connected message.
        await stream._connect_indexer(indexer.id)
        connected_message = await stream.__anext__()

        if not isinstance(connected_message, IndexerConnected):
            raise RuntimeError(f"Could not connect indexer {indexer.id}")

        # Yield stream to the caller.
        yield stream

        # Cleanup channel after the user finished.
        channel.close()


class IndexerStream:
    def __init__(self, channel: Channel, iter) -> None:
        self._chan = channel
        self._iter = iter.__aiter__()

    async def ack_block(self, block_hash: bytes):
        ack = indexer_service_pb2.AckBlock(hash=block_hash)
        request = indexer_service_pb2.ConnectIndexerRequest(ack=ack)
        await self._chan.put(request)

    async def _connect_indexer(self, id: str):
        connect = indexer_service_pb2.ConnectIndexer(id=id)
        request = indexer_service_pb2.ConnectIndexerRequest(connect=connect)
        await self._chan.put(request)

    def __aiter__(self):
        return self

    async def __anext__(self):
        response = await self._iter.__anext__()
        return self._parse_response(response)

    def _parse_response(self, response):
        if response.HasField("connected"):
            return IndexerConnected.from_proto(response.connected)

        if response.HasField("new_block"):
            return NewBlock.from_proto(response.new_block)

        if response.HasField("reorg"):
            return Reorg.from_proto(response.reorg)

        if response.HasField("new_events"):
            return NewEvents.from_proto(response.new_events)

        raise RuntimeError(f"unknown ConnectIndexerResponse message:\n{response}")
