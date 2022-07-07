import pytest
from pymongo import MongoClient

from apibara.indexer.storage import IndexerStorage


@pytest.fixture
def player():
    return {
        "player_name": "Alice",
        "address": "0xA",
        "player_since": 2022,
    }


@pytest.fixture
def extra_player():
    return {
        "player_name": "Bob",
        "address": "0xB",
        "player_since": 2021,
    }


@pytest.fixture()
def storage() -> IndexerStorage:
    url = "mongodb://apibara:apibara@localhost:27017"
    # Remove previous test data
    db = MongoClient(url)
    db.drop_database("test_storage")
    return IndexerStorage(url, "test-storage")


@pytest.mark.asyncio
async def test_insert_one(storage: IndexerStorage, player):
    with storage.create_storage_for_block(100) as s:
        await s.insert_one("players", player)

    with storage.create_storage_for_block(200) as s:
        alice = await s.find_one("players", {"address": "0xA"})
        assert alice is not None
        bob = await s.find_one("players", {"address": "0xB"})
        assert bob is None


@pytest.mark.asyncio
async def test_insert_many(storage: IndexerStorage, player, extra_player):
    with storage.create_storage_for_block(100) as s:
        await s.insert_many("players", [player, extra_player])
        bob = await s.find_one("players", {"address": "0xB"})
        assert bob is not None


@pytest.mark.asyncio
async def test_find_one_and_replace(storage: IndexerStorage, player):
    with storage.create_storage_for_block(100) as s:
        await s.insert_one("players", player)

    with storage.create_storage_for_block(200) as s:
        await s.find_one_and_replace(
            "players",
            {"address": "0xA"},
            {
                "player_name": "Arnold",
                "address": "0xA",
            },
            upsert=False,
        )

    with storage.create_storage_for_block(300) as s:
        arnold = await s.find_one("players", {"address": "0xA"})
        assert arnold is not None
        assert arnold["player_name"] == "Arnold"


@pytest.mark.asyncio
async def test_find_one_and_update(storage: IndexerStorage, player):
    with storage.create_storage_for_block(100) as s:
        await s.insert_one("players", player)

    with storage.create_storage_for_block(200) as s:
        old = await s.find_one_and_update(
            "players", {"address": "0xA"}, {"$set": {"player_name": "Arnold"}}
        )
        assert old["player_name"] == "Alice"

    with storage.create_storage_for_block(300) as s:
        arnold = await s.find_one("players", {"address": "0xA"})
        assert arnold["player_name"] == "Arnold"
