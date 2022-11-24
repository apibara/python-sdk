import json
from pathlib import Path

import pytest

from apibara.indexer.storage import IndexerStorage


def fixture_path(filename):
    return Path(__file__).parent / "fixtures" / filename


def load_json_fixture(filename):
    with open(fixture_path(filename)) as f:
        return json.load(f)


@pytest.fixture(scope="function")
def storage():
    connection_url = "mongodb://apibara:apibara@localhost:27017"
    storage = IndexerStorage(connection_url, "python-sdk-test-db")
    yield storage
    # cleanup database
    storage.drop_database()
