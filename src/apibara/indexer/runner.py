"""Apibara indexer runner."""

import asyncio
import warnings
from dataclasses import dataclass
from typing import Generic, List, Optional

from grpc_requests.aio import AsyncClient

from apibara.indexer.handler import (BlockHandler, MessageHandler,
                                     NewEventsHandler, ReorgHandler,
                                     UserContext)
from apibara.indexer.storage import IndexerStorage
from apibara.logging import logger
from apibara.model import BlockHeader, EventFilter, NewBlock, NewEvents


@dataclass
class IndexerRunnerConfiguration:
    """IndexerRunner configuration.

    Parameters
    ----------
    apibara_url:
        url of the Apibara stream.
    apibara_ssl:
        flag to connect using SSL.
    storage_url:
        MongoDB connection string, used to store the indexer  data and state.
    """

    apibara_url: Optional[str] = None
    apibara_ssl: bool = True
    rpc_url: Optional[str] = None
    storage_url: Optional[str] = None


class IndexerRunner(Generic[UserContext]):
    """Run an indexer, listening for new events and calling the provided callbacks.

    Parameters
    ----------
    indexer_id:
        unique id of this indexer. Used when persisting state.
    new_events_handler:
        async function called for each new block containing indexed events.
    reset_state:
        flag to restart the indexer from the beginning.
    config:
        options to set the input stream and connection string.
    """

    def __init__(
        self,
        *,
        indexer_id: str,
        new_events_handler: NewEventsHandler,
        reset_state: bool = False,
        config: Optional[IndexerRunnerConfiguration] = None,
    ) -> None:
        if config is None:
            config = IndexerRunnerConfiguration()
        self._reset_state = reset_state
        self._indexer_id = indexer_id
        self._config = config
        self._new_events_handler = new_events_handler
        self._block_handler = None
        self._pending_events_handler = None
        self._reorg_handler = None
        self._context = None
        self._indexer_storage = IndexerStorage(
            self._config.storage_url, self._indexer_id
        )

        self._indexer_config = None
        self._event_name_map = dict()

    def create_if_not_exists(
        self,
        filters: Optional[List[EventFilter]] = None,
        index_from_block: Optional[int] = None,
    ):
        warnings.warn(
            "create_if_not_exist should not be used. Use add_event_filters.",
            DeprecationWarning,
        )
        self.add_event_filters(filters, index_from_block)

    def add_event_filters(
        self,
        filters: Optional[List[EventFilter]] = None,
        index_from_block: Optional[int] = None,
    ):
        """Add the initial event filters.

        Parameters
        ----------
        filters:
            a list of EventFilter
        index_from_block:
            start indexing from the given block.
        """
        self._indexer_config = {
            "filters": filters,
            "index_from_block": index_from_block,
        }

    def set_context(self, context: UserContext):
        """Set the context object used to share information between handlers."""
        self._context = context

    def add_block_handler(self, block_handler: BlockHandler) -> None:
        """Add a callback called every time there is a new block."""
        self._block_handler = block_handler

    def add_pending_events_handler(
        self, events_handler: NewEventsHandler, interval_seconds: Optional[int] = None
    ) -> None:
        """Add a callback called every time there is a new pending block."""
        if interval_seconds is None:
            interval_seconds = 5
        self._pending_events_handler = (events_handler, interval_seconds)

    def add_reorg_handler(self, reorg_handler: ReorgHandler) -> None:
        """Add a callback called every time there is a chain reorganization."""
        self._reorg_handler = reorg_handler

    async def run(self):
        """Run the indexer until stopped."""
        # self._print_deprecation_notice()
        self._check_config()
        if self._reset_state:
            self._delete_old_state()
        self._write_initial_state()
        await self._do_run()

    def _check_config(self):
        if self._config is None:
            raise RuntimeError("must provide config to IndexerRunner")

        if self._config.apibara_url is None:
            raise RuntimeError("must provide an apibara_url in config")

        if self._config.storage_url is None:
            raise RuntimeError("must provide a storage_url in config")

    def _print_deprecation_notice(self):
        warnings.warn(
            "IndexerRunner is deprecated and will be removed in the next release.",
            DeprecationWarning,
        )

    def _delete_old_state(self):
        self._indexer_storage.drop_database()

    def _write_initial_state(self):
        self._indexer_storage.initialize(
            self._indexer_config["index_from_block"], self._indexer_config["filters"]
        )

    async def _do_run(self):
        client = AsyncClient(self._config.apibara_url, ssl=self._config.apibara_ssl)

        node_service = await client.service("apibara.node.v1alpha1.Node")

        starting_sequence = self._indexer_storage.starting_sequence()
        stream_messages_request = {
            "starting_sequence": starting_sequence,
        }
        pending_handler = None
        if self._pending_events_handler is not None:
            pending_handler = self._pending_events_handler[0]
            pending_block_interval_seconds = self._pending_events_handler[1]
            stream_messages_request[
                "pending_block_interval_seconds"
            ] = pending_block_interval_seconds
        logger.debug("starting stream")
        message_stream = await node_service.StreamMessages(stream_messages_request)

        starting_filters = self._indexer_storage.event_filters()

        message_handler = MessageHandler(
            data_handler=self._new_events_handler,
            block_handler=self._block_handler,
            reorg_handler=self._reorg_handler,
            pending_handler=pending_handler,
            context=self._context,
            storage=self._indexer_storage,
            starting_filters=starting_filters,
        )

        if starting_sequence is not None:
            logger.debug("invalidate pending data")
            # Remove any pending data from the previous run
            self._indexer_storage.invalidate(starting_sequence)

        while True:
            # We expect one heartbeat every 30 seconds
            # Add 15 seconds of buffer, we the stream doesn't produce any message
            # in this timeframe then there is something wrong with the stream.
            message = await asyncio.wait_for(message_stream.__anext__(), timeout=45.0)

            if "data" in message:
                logger.debug("received data")
                block = message["data"]["data"]
                await message_handler.handle_data(block)

            elif "invalidate" in message:
                logger.debug("received invalidate")
                invalidate = message["invalidate"]
                await message_handler.handle_invalidate(invalidate)

            elif "pending" in message:
                logger.debug("received pending")
                block = message["pending"]["data"]
                await message_handler.handle_pending(block)
