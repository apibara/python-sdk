"""Connect and interact with the Apibara server."""

from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

import grpc

from apibara.indexer.indexer import IndexerClient

_DEFAULT_APIBARA_SERVER_URL = "localhost:7171"


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
