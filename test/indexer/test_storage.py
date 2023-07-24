from test.conftest import storage

import pytest

from apibara.indexer.storage import IndexerStorage
from apibara.starknet import starknet_cursor


@pytest.mark.asyncio
@pytest.mark.skip(reason="Docker permission in CI")
async def test_insert_one(storage: IndexerStorage):
    with storage.create_storage_for_block(starknet_cursor(100)) as s:
        await s.insert_one("capibaras", {"name": "bob", "age": 3})

    with storage.create_storage_for_block(101) as s:
        capybaras = await s.find("capibaras", {})
        capybaras = list(capybaras)
        assert len(capybaras) == 1


@pytest.mark.asyncio
@pytest.mark.skip(reason="Docker permission in CI")
async def test_insert_many(storage: IndexerStorage):
    with storage.create_storage_for_block(starknet_cursor(100)) as s:
        await s.insert_many(
            "capibaras",
            [
                {"name": "bob", "age": 3},
                {"name": "charlie", "age": 4},
            ],
        )

    with storage.create_storage_for_block(starknet_cursor(101)) as s:
        capybaras = await s.find("capibaras", {})
        capybaras = list(capybaras)
        assert len(capybaras) == 2


@pytest.mark.asyncio
@pytest.mark.skip(reason="Docker permission in CI")
async def test_delete_one(storage: IndexerStorage):
    with storage.create_storage_for_block(starknet_cursor(100)) as s:
        await s.insert_many(
            "capibaras",
            [
                {"name": "bob", "age": 3},
                {"name": "charlie", "age": 4},
            ],
        )

    with storage.create_storage_for_block(starknet_cursor(100)) as s:
        await s.delete_one("capibaras", {"age": {"$gte": 4}})

    with storage.create_storage_for_block(starknet_cursor(102)) as s:
        capybaras = await s.find("capibaras", {})
        capybaras = list(capybaras)
        assert len(capybaras) == 1


@pytest.mark.asyncio
@pytest.mark.skip(reason="Docker permission in CI")
async def test_delete_many(storage: IndexerStorage):
    with storage.create_storage_for_block(starknet_cursor(100)) as s:
        await s.insert_many(
            "capibaras",
            [
                {"name": "bob", "age": 3},
                {"name": "charlie", "age": 4},
                {"name": "dylan", "age": 8},
            ],
        )

    with storage.create_storage_for_block(starknet_cursor(101)) as s:
        await s.delete_many("capibaras", {"age": {"$gte": 4}})

    with storage.create_storage_for_block(starknet_cursor(102)) as s:
        capybaras = await s.find("capibaras", {})
        capybaras = list(capybaras)
        assert len(capybaras) == 1


@pytest.mark.asyncio
@pytest.mark.skip(reason="Docker permission in CI")
async def test_find_one_and_replace(storage: IndexerStorage):
    with storage.create_storage_for_block(starknet_cursor(100)) as s:
        await s.insert_many(
            "capibaras",
            [
                {"name": "bob", "age": 3},
                {"name": "charlie", "age": 4},
                {"name": "dylan", "age": 8},
            ],
        )

    with storage.create_storage_for_block(starknet_cursor(101)) as s:
        await s.find_one_and_replace(
            "capibaras", {"name": "bob"}, {"name": "bob", "age": 10}
        )

    with storage.create_storage_for_block(starknet_cursor(102)) as s:
        bob = await s.find_one("capibaras", {"name": "bob"})
        assert bob["age"] == 10


@pytest.mark.asyncio
@pytest.mark.skip(reason="Docker permission in CI")
async def test_find_one_and_update(storage: IndexerStorage):
    with storage.create_storage_for_block(starknet_cursor(100)) as s:
        await s.insert_many(
            "capibaras",
            [
                {"name": "bob", "age": 3},
                {"name": "charlie", "age": 4},
                {"name": "dylan", "age": 8},
            ],
        )

    with storage.create_storage_for_block(starknet_cursor(101)) as s:
        await s.find_one_and_update("capibaras", {"name": "bob"}, {"$set": {"age": 10}})

    with storage.create_storage_for_block(starknet_cursor(102)) as s:
        bob = await s.find_one("capibaras", {"name": "bob"})
        assert bob["age"] == 10


@pytest.mark.asyncio
@pytest.mark.skip(reason="Docker permission in CI")
async def test_invalidate(storage: IndexerStorage):
    with storage.create_storage_for_block(starknet_cursor(100)) as s:
        await s.insert_many(
            "capibaras",
            [
                {"name": "bob", "age": 3},
                {"name": "charlie", "age": 4},
                {"name": "dylan", "age": 8},
            ],
        )

    with storage.create_storage_for_block(starknet_cursor(101)) as s:
        await s.insert_many(
            "capibaras",
            [
                {"name": "elon", "age": 3},
                {"name": "fran", "age": 4},
                {"name": "galois", "age": 8},
            ],
        )
        await s.delete_one("capibaras", {"name": "bob"})
        await s.find_one_and_update(
            "capibaras", {"name": "charlie"}, {"$set": {"age": 5}}
        )

    with storage.create_storage_for_block(starknet_cursor(102)) as s:
        await s.delete_one("capibaras", {"name": "fran"})
        await s.find_one_and_update(
            "capibaras", {"name": "charlie"}, {"$set": {"age": 6}}
        )

    with storage.create_storage_for_block(starknet_cursor(103)) as s:
        await s.delete_one("capibaras", {"name": "galois"})
        await s.find_one_and_update(
            "capibaras", {"name": "dylan"}, {"$set": {"age": 9}}
        )

    storage.invalidate(starknet_cursor(101))

    with storage.create_storage_for_block(starknet_cursor(102)) as s:
        capybaras = await s.find("capibaras", {})
        capybaras = list(capybaras)
        names = sorted([c["name"] for c in capybaras])
        assert names == ["charlie", "dylan", "elon", "fran", "galois"]
        charlie = await s.find_one("capibaras", {"name": "charlie"})
        assert charlie["age"] == 5
