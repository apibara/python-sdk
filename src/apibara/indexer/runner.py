import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, Optional, TypeVar
from urllib.request import DataHandler

from grpc import ssl_channel_credentials
from grpc.aio import insecure_channel, secure_channel

from apibara.indexer.indexer import Indexer
from apibara.indexer.info import Info, UserContext
from apibara.indexer.storage import Filter, IndexerStorage
from apibara.protocol import StreamService


@dataclass
class IndexerRunnerConfiguration:
    """IndexerRunner configuration.

    Parameters
    ----------
    stream_url:
        url of the Apibara stream.
    stream_ssl:
        flag to connect using SSL.
    storage_url:
        MongoDB connection string, used to store the indexer  data and state.
    """

    stream_url: Optional[str] = None
    stream_ssl: bool = True
    storage_url: Optional[str] = None


class IndexerRunner(Generic[UserContext, Filter]):
    """Run an indexer, listening for new data and calling the provided callbacks.

    Parameters
    ----------
    reset_state:
        flag to restart the indexer from the beginning.
    config:
        options to set the input stream and connection string.
    """

    def __init__(
        self,
        *,
        reset_state: bool = False,
        config: Optional[IndexerRunnerConfiguration] = None,
    ) -> None:
        if config is None:
            config = IndexerRunnerConfiguration()
        self._reset_state = reset_state
        self._config = config
        self._indexer_id = None
        self._indexer_storage = None

    async def run(self, indexer: Indexer, *, ctx: Optional[UserContext] = None):
        """Run the indexer until stopped."""
        self._check_config()
        self._setup_storage(indexer)
        await self._do_run(indexer, ctx)

    def _check_config(self):
        if self._config is None:
            raise RuntimeError("must provide config to IndexerRunner")

        if self._config.stream_url is None:
            raise RuntimeError("must provide a stream_url in config")

        if self._config.storage_url is None:
            raise RuntimeError("must provide a storage_url in config")

    def _setup_storage(self, indexer: Indexer):
        self._indexer_id = indexer.indexer_id()
        self._indexer_storage = IndexerStorage(
            self._config.storage_url, self._indexer_id
        )

    async def _do_run(self, indexer: Indexer, ctx: Optional[UserContext] = None):
        channel = self._channel()
        retry_count = 0

        # TODO: maybe reset state
        while True:
            try:
                (client, stream) = StreamService(channel).stream_data()

                # send initial config
                # TODO: load it from storage if already exists
                initial_config = indexer.initial_configuration()
                await client.configure(
                    filter=initial_config.filter.encode(),
                    finality=initial_config.finality,
                    cursor=initial_config.starting_cursor,
                    batch_size=1,
                )

                async for message in stream:
                    retry_count = 0
                    if message.data is not None:
                        assert (
                            len(message.data.data) <= 1
                        ), "indexer runner requires batch_size == 1"

                        for batch in message.data.data:
                            with self._indexer_storage.create_storage_for_data(
                                message.data.end_cursor
                            ) as storage:
                                decoded_data = indexer.parse_data(batch)
                                info = Info(context=ctx, storage=storage)
                                await indexer.handle_data(info, decoded_data)
                                # TODO: check if user updated filter

                    elif message.invalidate is not None:
                        with self._indexer_storage.create_storage_for_invalidate(
                            message.invalidate.cursor
                        ) as storage:
                            info = Info(context=ctx, storage=storage)
                            await indexer.handle_invalidate(
                                info, message.invalidate.cursor
                            )

            except Exception as exc:
                retry_count += 1
                reconnect = await indexer.handle_reconnect(exc, retry_count)

                if not reconnect.reconnect:
                    raise exc

    def _channel(self):
        if self._config.stream_ssl:
            return secure_channel(self._config.stream_url, ssl_channel_credentials())
        return insecure_channel(self._config.stream_url)
