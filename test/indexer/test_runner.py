import asyncio
from test.conftest import mongo_db
from unittest.mock import ANY, MagicMock, call

import pytest
from pymongo import MongoClient

from apibara.indexer import (
    IndexerConfiguration,
    IndexerRunner,
    IndexerRunnerConfiguration,
)
from apibara.protocol.proto.stream_pb2 import (
    Cursor,
    Data,
    DataFinality,
    StreamDataResponse,
)
from apibara.starknet import EventFilter, Filter, StarkNetIndexer, starknet_cursor
from apibara.starknet.proto.starknet_pb2 import Block, BlockHeader


class MockIndexer(StarkNetIndexer):
    def indexer_id(self):
        return "test"

    def initial_configuration(self):
        return IndexerConfiguration(
            filter=Filter().with_header(weak=True),
            starting_cursor=starknet_cursor(0),
            finality=DataFinality.DATA_STATUS_PENDING,
        )

    async def handle_data(self, info, data):
        await self._handle_data(info, data)

    async def handle_pending_data(self, info, data):
        await self._handle_data(info, data)

    async def _handle_data(self, info, data):
        await info.storage.insert_one(
            "blocks", {"block_number": data.header.block_number}
        )


def future(value):
    fut = asyncio.Future()
    fut.set_result(value)
    return fut


class MockStreamClient:
    pass


class MockDataStream:
    def __init__(self):
        self.q = asyncio.Queue()

    def put_iter(self, items):
        for item in items:
            self.q.put_nowait(item)

    def __aiter__(self):
        return self

    async def __anext__(self):
        v = await self.q.get()
        if v is None:
            raise StopAsyncIteration

        return v


class MockIndexerRunner(IndexerRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MockStreamClient()
        self.stream = MockDataStream()

    def _stream_data(self):
        return (self.client, self.stream, None)


def new_data(
    start_block, end_block, stream_id=1, finality=DataFinality.DATA_STATUS_FINALIZED
):
    start = starknet_cursor(start_block)
    end = starknet_cursor(end_block)
    block = Block(header=BlockHeader(block_number=end_block))
    return StreamDataResponse(
        stream_id=stream_id,
        data=Data(
            cursor=start,
            end_cursor=end,
            finality=finality,
            data=[block.SerializeToString()],
        ),
    )


@pytest.mark.asyncio
async def test_runner_invokes_indexer(mongo_db):
    runner = MockIndexerRunner(
        reset_state=True,
        config=IndexerRunnerConfiguration(
            stream_url="http://localhost:5000", storage_url=mongo_db
        ),
    )

    indexer = MockIndexer()
    indexer.handle_data = MagicMock(return_value=future(None))

    runner.client.configure = MagicMock(return_value=future(None))
    runner.stream.put_iter(
        [
            new_data(0, 1, finality=DataFinality.DATA_STATUS_ACCEPTED),
            new_data(1, 2, finality=DataFinality.DATA_STATUS_ACCEPTED),
            new_data(2, 3, finality=DataFinality.DATA_STATUS_ACCEPTED),
            None,
        ]
    )

    await runner.run(indexer)

    indexer.handle_data.assert_called()
    runner.client.configure.assert_called_once()


@pytest.mark.asyncio
async def test_invalidate_between_pending_blocks(mongo_db):
    runner = MockIndexerRunner(
        reset_state=True,
        config=IndexerRunnerConfiguration(
            stream_url="http://localhost:5000", storage_url=mongo_db
        ),
    )

    indexer = MockIndexer()
    runner.client.configure = MagicMock(return_value=future(None))

    runner.stream.put_iter(
        [
            new_data(0, 1, finality=DataFinality.DATA_STATUS_ACCEPTED),
            new_data(1, 2, finality=DataFinality.DATA_STATUS_ACCEPTED),
            new_data(2, 3, finality=DataFinality.DATA_STATUS_ACCEPTED),
            # send a bunch of repeated pending blocks
            new_data(3, 4, finality=DataFinality.DATA_STATUS_PENDING),
            new_data(3, 4, finality=DataFinality.DATA_STATUS_PENDING),
            new_data(3, 4, finality=DataFinality.DATA_STATUS_PENDING),
            new_data(3, 4, finality=DataFinality.DATA_STATUS_PENDING),
            # send the same block, but accepted
            new_data(3, 4, finality=DataFinality.DATA_STATUS_ACCEPTED),
            None,
        ]
    )

    await runner.run(indexer)

    client = MongoClient(mongo_db)
    db = client["test"]
    col = db["blocks"]
    docs = [d for d in col.find()]
    assert len(docs) == 4


@pytest.mark.asyncio
async def test_reconnect_to_avoid_disconnect(mongo_db):
    runner = MockIndexerRunner(
        reset_state=True,
        _reconnect_to_avoid_disconnection=5,
        config=IndexerRunnerConfiguration(
            stream_url="http://localhost:5000", storage_url=mongo_db
        ),
    )

    indexer = MockIndexer()
    indexer.handle_data = MagicMock(return_value=future(None))

    runner.client.configure = MagicMock(return_value=future(None))
    data = [
        new_data(i, i + 1, finality=DataFinality.DATA_STATUS_ACCEPTED)
        for i in range(0, 10)
    ]
    runner.stream.put_iter(data + [None])

    await runner.run(indexer)

    indexer.handle_data.assert_called()
    runner.client.configure.assert_has_calls(
        [
            call(filter=ANY, finality=ANY, cursor=starknet_cursor(0), batch_size=1),
            call(filter=ANY, finality=ANY, cursor=starknet_cursor(5), batch_size=1),
            call(filter=ANY, finality=ANY, cursor=starknet_cursor(10), batch_size=1),
        ]
    )


@pytest.mark.asyncio
async def test_reconnect_to_avoid_disconnect_does_not_count_pending_blocks(mongo_db):
    runner = MockIndexerRunner(
        reset_state=True,
        _reconnect_to_avoid_disconnection=5,
        config=IndexerRunnerConfiguration(
            stream_url="http://localhost:5000", storage_url=mongo_db
        ),
    )

    indexer = MockIndexer()
    indexer.handle_data = MagicMock(return_value=future(None))
    indexer.handle_pending_data = MagicMock(return_value=future(None))

    runner.client.configure = MagicMock(return_value=future(None))
    data = (
        [
            new_data(i, i + 1, finality=DataFinality.DATA_STATUS_ACCEPTED)
            for i in range(0, 5)
        ]
        + [
            new_data(5, 6, finality=DataFinality.DATA_STATUS_PENDING)
            for i in range(0, 10)
        ]
        + [
            new_data(i, i + 1, finality=DataFinality.DATA_STATUS_ACCEPTED)
            for i in range(5, 10)
        ]
    )
    runner.stream.put_iter(data + [None])

    await runner.run(indexer)

    indexer.handle_data.assert_called()
    indexer.handle_pending_data.assert_called()

    runner.client.configure.assert_has_calls(
        [
            call(filter=ANY, finality=ANY, cursor=starknet_cursor(0), batch_size=1),
            call(filter=ANY, finality=ANY, cursor=starknet_cursor(5), batch_size=1),
            call(filter=ANY, finality=ANY, cursor=starknet_cursor(10), batch_size=1),
        ]
    )
