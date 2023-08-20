import json
from pathlib import Path

import pytest
from testcontainers.mongodb import MongoDbContainer

from apibara.indexer.storage import IndexerStorage


def fixture_path(filename):
    return Path(__file__).parent / "fixtures" / filename


def load_json_fixture(filename):
    with open(fixture_path(filename)) as f:
        return json.load(f)


@pytest.fixture(scope="function")
def storage():
    with MongoDbContainer("mongo:latest") as mongo:
        connection_url = mongo.get_connection_url()
        storage = IndexerStorage(connection_url, "python-sdk-test-db")
        yield storage
        # cleanup database
        storage.drop_database()


@pytest.fixture(scope="function")
def mongo_db():
    with MongoDbContainer("mongo:latest") as mongo:
        yield mongo.get_connection_url()
