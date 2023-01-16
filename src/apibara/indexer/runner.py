import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Generic, List, Optional, Tuple

from grpc import ssl_channel_credentials
from grpc.aio import insecure_channel, secure_channel

from apibara.indexer.indexer import Indexer
from apibara.indexer.info import Info, UserContext
from apibara.indexer.storage import Filter, IndexerStorage
from apibara.protocol import StreamService
from apibara.protocol.proto.stream_pb2 import DataFinality

logger = logging.getLogger(__name__)


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
    client_options:
        list of options passed to the gRPC channel.
    """

    def __init__(
        self,
        *,
        reset_state: bool = False,
        config: Optional[IndexerRunnerConfiguration] = None,
        client_options: Optional[List[Tuple[str, Any]]] = None,
    ) -> None:
        if config is None:
            config = IndexerRunnerConfiguration()
        self._reset_state = reset_state
        self._config = config
        self._indexer_id = None
        self._indexer_storage = None
        self._client_options = client_options

    async def run(self, indexer: Indexer, *, ctx: Optional[UserContext] = None):
        """Run the indexer until stopped."""
        self._check_config()
        self._setup_storage(indexer)
        self._maybe_reset_state()
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

    def _maybe_reset_state(self):
        if self._reset_state:
            logger.debug("reset state")
            self._indexer_storage.drop_database()

    async def _do_run(self, indexer: Indexer, ctx: Optional[UserContext] = None):
        self._retry_count = 0

        logger.debug("starting indexer")
        while True:
            try:
                await self._connect_and_stream(indexer, ctx)
            except Exception as exc:
                logger.debug("indexer exception %A", exc)
                self._retry_count += 1
                reconnect = await indexer.handle_reconnect(exc, self._retry_count)

                if not reconnect.reconnect:
                    raise

    async def _connect_and_stream(self, indexer: Indexer, ctx: Optional[UserContext]):
        channel = self._channel()
        (client, stream) = StreamService(channel).stream_data()

        config = indexer.initial_configuration()
        has_stored = self._indexer_storage.update_with_stored_configuration(config)
        if has_stored:
            # invalidate old pending data, if any
            self._indexer_storage.invalidate(config.starting_cursor)

        logger.debug("indexer configuration read")

        await client.configure(
            filter=config.filter.encode(),
            finality=config.finality,
            cursor=config.starting_cursor,
            batch_size=1,
        )

        logger.debug("indexer configuration sent")

        previous_end_cursor = None
        pending_received = False
        async for message in stream:
            logger.debug("received message")
            self._retry_count = 0
            if message.data is not None:
                assert (
                    len(message.data.data) <= 1
                ), "indexer runner requires batch_size == 1"

                # invalidate any pending data, if any
                if pending_received and previous_end_cursor is not None:
                    self._indexer_storage.invalidate(previous_end_cursor)

                is_pending = message.data.finality == DataFinality.DATA_STATUS_PENDING
                pending_received = is_pending

                for batch in message.data.data:
                    with self._indexer_storage.create_storage_for_data(
                        message.data.end_cursor
                    ) as storage:
                        decoded_data = indexer.decode_data(batch)
                        info = Info(context=ctx, storage=storage)
                        if is_pending:
                            await indexer.handle_pending_data(info, decoded_data)
                        else:
                            await indexer.handle_data(info, decoded_data)
                        # TODO: check if user updated filter

                if not is_pending:
                    previous_end_cursor = message.data.end_cursor

            elif message.invalidate is not None:
                with self._indexer_storage.create_storage_for_invalidate(
                    message.invalidate.cursor
                ) as storage:
                    info = Info(context=ctx, storage=storage)
                    await indexer.handle_invalidate(info, message.invalidate.cursor)
                previous_end_cursor = message.invalidate.cursor

    def _channel(self):
        if self._config.stream_ssl:
            return secure_channel(
                self._config.stream_url,
                ssl_channel_credentials(),
                options=self._client_options,
            )
        return insecure_channel(self._config.stream_url, options=self._client_options)
