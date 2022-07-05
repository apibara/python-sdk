"""Connect and interact with the Apibara server."""

from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional
import grpc

import apibara.application.indexer_service_pb2 as indexer_service_pb2
from apibara.indexer.indexer import IndexerClient
from apibara.starknet import get_selector_from_name


_DEFAULT_APIBARA_SERVER_URL = "localhost:7171"


def contract_event_filter(name, address=None):
    """
    Returns the `EventFilter` for the given event.

    Optionally filter by the contract emitting the event.
    """
    if address is None:
        address = b""

    if isinstance(address, str):
        address = bytes.fromhex(address.replace("0x", ""))

    topic_hex = hex(get_selector_from_name(name))[2:]
    # fromhex requires an even number of digits
    if len(topic_hex) % 2 == 1:
        topic_hex = "0" + topic_hex
    topic_value = bytes.fromhex(topic_hex)

    topics = indexer_service_pb2.Topic(
        choices=[indexer_service_pb2.TopicValue(value=topic_value)]
    )

    return indexer_service_pb2.EventFilter(
        address=address,
        topics=[topics],
    )


class Client:
    """Apibara client."""

    @staticmethod
    @asynccontextmanager
    async def connect(url: Optional[str] = None) -> AsyncIterator["Client"]:
        if url is None:
            url = _DEFAULT_APIBARA_SERVER_URL
        async with grpc.aio.insecure_channel(url) as channel:
            yield Client(channel)

    def __init__(self, channel) -> None:
        self._channel = channel

    def indexer_client(self) -> IndexerClient:
        return IndexerClient(self._channel)
