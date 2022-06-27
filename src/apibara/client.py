"""Connect and interact with the Apibara server."""

from contextlib import asynccontextmanager

import grpc
from aiochannel import Channel

import apibara.application.indexer_service_pb2 as indexer_service_pb2
import apibara.application.indexer_service_pb2_grpc as indexer_service_pb2_grpc
from apibara.model import Indexer, IndexerConnected, NewBlock, NewEvents, Reorg
from apibara.starknet import get_selector_from_name


DEFAULT_APIBARA_SERVER_URL = "localhost:7171"


def contract_event_filter(name, address=None):
    """
    Returns the `EventFilter` for the given event.

    Optionally filter by the contract emitting the event.
    """
    if address is None:
        address = b""

    if isinstance(address, str):
        address = bytes.fromhex(address.replace("0x", ""))

    topic_value = bytes.fromhex(hex(get_selector_from_name(name))[2:])

    topics = indexer_service_pb2.Topic(
        choices=[indexer_service_pb2.TopicValue(value=topic_value)]
    )

    return indexer_service_pb2.EventFilter(
        address=address,
        topics=[topics],
    )


class IndexerManagerClient:
    """Client to manage an indexer."""

    @staticmethod
    @asynccontextmanager
    async def insecure_channel(url) -> "IndexerManagerClient":
        async with grpc.aio.insecure_channel(url) as channel:
            yield IndexerManagerClient(channel)

    def __init__(self, channel) -> None:
        self._channel = channel
        self._stub = indexer_service_pb2_grpc.IndexerManagerStub(self._channel)

    async def get_indexer(self, id):
        try:
            response = await self._stub.GetIndexer(
                indexer_service_pb2.GetIndexerRequest(id=id)
            )
            if response and response.indexer and response.indexer.id:
                return Indexer.from_proto(response.indexer)
        except grpc.aio.AioRpcError as ex:
            if ex.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise

    async def create_indexer(self, id, index_from_block, filters):
        if not isinstance(filters, list):
            filters = [filters]

        response = await self._stub.CreateIndexer(
            indexer_service_pb2.CreateIndexerRequest(
                id=id, index_from_block=index_from_block, filters=filters
            )
        )

        if response and response.indexer:
            return Indexer.from_proto(response.indexer)

    async def delete_indexer(self, id):
        response = await self._stub.DeleteIndexer(
            indexer_service_pb2.DeleteIndexerRequest(id=id)
        )

        if response and response.indexer:
            return Indexer.from_proto(response.indexer)

    async def list_indexer(self):
        response = await self._stub.ListIndexer(
            indexer_service_pb2.ListIndexerRequest()
        )

        return [Indexer.from_proto(ix) for ix in response.indexers]

    async def connect_indexer(self):
        client = ConnectIndexerClient()
        response_iter = self._stub.ConnectIndexer(client._chan)

        return ConnectIndexerStream(response_iter), client


class ConnectIndexerClient:
    def __init__(self) -> None:
        self._chan = Channel()

    async def connect_indexer(self, id):
        connect = indexer_service_pb2.ConnectIndexer(id=id)
        request = indexer_service_pb2.ConnectIndexerRequest(connect=connect)
        await self._chan.put(request)

    async def ack_block(self, block_hash):
        ack = indexer_service_pb2.AckBlock(hash=block_hash)
        request = indexer_service_pb2.ConnectIndexerRequest(ack=ack)
        await self._chan.put(request)


class ConnectIndexerStream:
    def __init__(self, iter) -> None:
        self._iter = iter.__aiter__()

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
