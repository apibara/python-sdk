from email.message import Message

import pytest

from apibara.indexer.handler import Info, MessageHandler, UserContext
from apibara.indexer.storage import IndexerStorage
from apibara.model import EventFilter, NewBlock, NewEvents
from tests.conftest import load_json_fixture, storage

transfer_filters = [
    EventFilter.from_event_name(
        "Transfer",
        address="0x07861c4e276294a7e859ff0ae2eec0c68300ad9cbb43219db907da9bad786488",
    ),
]


class MockHandler:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.data_called = False
        self.block_called = False
        self.reorg_called = False
        self.pending_called = False

    async def data_handler(self, info: Info, data: NewEvents):
        self.data_called = True

        await info.storage.insert_one("events", {"test": True})

    async def block_handler(self, info: Info, data: NewBlock):
        self.block_called = True
        await info.storage.insert_one("blocks", {"number": data.new_head.number})

    async def reorg_handler(self, info: Info, data: int):
        self.reorg_called = True

    async def pending_handler(self, info: Info, data: NewEvents):
        self.pending_called = True
        await info.storage.insert_one(
            "pendings", {"count": len(data.events), "number": data.block.number}
        )


@pytest.mark.asyncio
async def test_invalidate_after_data(storage: IndexerStorage):
    context = dict()

    mock = MockHandler()
    storage.initialize(11000, [])

    handler = MessageHandler(
        data_handler=mock.data_handler,
        block_handler=mock.block_handler,
        reorg_handler=mock.reorg_handler,
        pending_handler=mock.pending_handler,
        context=context,
        storage=storage,
        starting_filters=transfer_filters,
    )

    data = load_json_fixture("block_11000.json")
    block = data["data"]["data"]

    await handler.handle_data(block)
    next_starting_sequence = storage.starting_sequence()
    assert next_starting_sequence == 11001

    assert mock.data_called
    assert mock.block_called
    assert not mock.pending_called
    assert not mock.reorg_called

    mock.reset()

    with storage.create_storage_for_block(11001) as s:
        blocks = await s.find("blocks", {})
        blocks = list(blocks)
        assert len(blocks) == 1

    await handler.handle_invalidate({"sequence": 11000})
    # invalidated all data _at and after_ 11000, so will restart from 11000
    next_starting_sequence = storage.starting_sequence()
    assert next_starting_sequence == 11000

    assert not mock.data_called
    assert not mock.block_called
    assert not mock.pending_called
    assert mock.reorg_called

    mock.reset()

    with storage.create_storage_for_block(11001) as s:
        blocks = await s.find("blocks", {})
        blocks = list(blocks)
        assert blocks == []


@pytest.mark.asyncio
async def test_pending_after_pending(storage: IndexerStorage):
    context = dict()

    mock = MockHandler()
    storage.initialize(11000, [])

    handler = MessageHandler(
        data_handler=mock.data_handler,
        block_handler=mock.block_handler,
        reorg_handler=mock.reorg_handler,
        pending_handler=mock.pending_handler,
        context=context,
        storage=storage,
        starting_filters=transfer_filters,
    )

    data = load_json_fixture("block_11000.json")
    block = data["data"]["data"]

    await handler.handle_pending(block)
    # pending blocks don't update starting sequence
    next_starting_sequence = storage.starting_sequence()
    assert next_starting_sequence == 11000

    assert not mock.data_called
    assert not mock.block_called
    assert mock.pending_called
    assert not mock.reorg_called

    mock.reset()

    with storage.create_storage_for_block(11000) as s:
        pendings = await s.find("pendings", {})
        pendings = list(pendings)
        assert len(pendings) == 1
        assert pendings[0]["count"] == 8
        assert pendings[0]["number"] == 11000

    await handler.handle_pending(block)
    # pending blocks don't update starting sequence
    next_starting_sequence = storage.starting_sequence()
    assert next_starting_sequence == 11000

    assert not mock.data_called
    assert not mock.block_called
    assert mock.pending_called
    assert not mock.reorg_called

    mock.reset()

    with storage.create_storage_for_block(11000) as s:
        pendings = await s.find("pendings", {})
        pendings = list(pendings)
        assert len(pendings) == 1
        assert pendings[0]["count"] == 8
        assert pendings[0]["number"] == 11000


@pytest.mark.asyncio
async def test_data_after_pending(storage: IndexerStorage):
    context = dict()

    mock = MockHandler()
    storage.initialize(11000, [])

    handler = MessageHandler(
        data_handler=mock.data_handler,
        block_handler=mock.block_handler,
        reorg_handler=mock.reorg_handler,
        pending_handler=mock.pending_handler,
        context=context,
        storage=storage,
        starting_filters=transfer_filters,
    )

    data = load_json_fixture("block_11000.json")
    block = data["data"]["data"]

    await handler.handle_pending(block)
    # pending blocks don't update starting sequence
    next_starting_sequence = storage.starting_sequence()
    assert next_starting_sequence == 11000

    assert not mock.data_called
    assert not mock.block_called
    assert mock.pending_called
    assert not mock.reorg_called

    mock.reset()

    with storage.create_storage_for_block(11000) as s:
        pendings = await s.find("pendings", {})
        pendings = list(pendings)
        assert len(pendings) == 1
        assert pendings[0]["count"] == 8
        assert pendings[0]["number"] == 11000

    await handler.handle_data(block)
    # data blocks do
    next_starting_sequence = storage.starting_sequence()
    assert next_starting_sequence == 11001

    assert mock.data_called
    assert mock.block_called
    assert not mock.pending_called
    assert not mock.reorg_called

    mock.reset()

    with storage.create_storage_for_block(11000) as s:
        pendings = await s.find("pendings", {})
        pendings = list(pendings)
        assert len(pendings) == 0
