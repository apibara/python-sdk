from contextlib import contextmanager
from typing import Any, Iterable, Iterator, List, Optional

from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.database import Database

from apibara.model import EventFilter

Document = dict[str, Any]
Filter = dict[str, Any]
Update = dict[str, Any]
Projection = dict[str, any]


class IndexerStorage:
    """Create instances of Storage."""

    def __init__(self, url: Optional[str], indexer_id: str) -> None:
        if url is None:
            raise ValueError("Storage url must be not None")

        self.db_name = indexer_id.replace("-", "_")
        self._indexer_id = indexer_id

        self._mongo = MongoClient(url)
        self.db = self._mongo[self.db_name]

    @contextmanager
    def create_storage_for_block(self, block_number: int) -> Iterator["Storage"]:
        with self._mongo.start_session() as session:
            yield Storage(self.db, session, block_number)
            self._update_indexed_to(block_number, session)

    def initialize(self, starting_sequence: int, filters: List[EventFilter]):
        existing = self.db["_apibara"].find_one({"indexer_id": self._indexer_id})
        if existing is not None:
            return
        self.db["_apibara"].insert_one(
            {
                "indexer_id": self._indexer_id,
                "indexed_to": starting_sequence,
                "filters": [f.to_json() for f in filters],
            }
        )

    def starting_sequence(self):
        state = self.db["_apibara"].find_one({"indexer_id": self._indexer_id})
        if state is None or state.get("indexed_to") is None:
            return None
        return state["indexed_to"] + 1

    def event_filters(self):
        state = self.db["_apibara"].find_one({"indexer_id": self._indexer_id})
        if state is None:
            raise RuntimeError("indexer state not found")
        return [EventFilter.from_json(j) for j in state["filters"]]

    def _set_event_filters(self, filters: List[EventFilter], session: ClientSession):
        """Set the indexer event filters, overriding the previous filters."""
        filters_docs = [f.to_json() for f in filters]
        self.db["_apibara"].update_one(
            {"indexer_id": self._indexer_id},
            {"$set": {"filters": filters_docs}},
            session=session,
        )

    def drop_database(self):
        self._mongo.drop_database(self.db_name)

    def _update_indexed_to(self, block_number: int, session: ClientSession):
        self.db["_apibara"].update_one(
            {"indexer_id": self._indexer_id},
            {"$set": {"indexed_to": block_number}},
            upsert=True,
            session=session,
        )


class Storage:
    """Chain-aware document storage."""

    def __init__(self, db: Database, session: ClientSession, block_number: int) -> None:
        self._db = db
        self._block_number = block_number
        self._session = session

    async def insert_one(self, collection: str, doc: Document):
        """Insert `doc` into `collection`."""
        self._add_chain_information(doc)
        self._db[collection].insert_one(doc, session=self._session)

    async def insert_many(self, collection: str, docs: Iterable[Document]):
        """Insert multiple `docs` into `collection`."""
        for doc in docs:
            self._add_chain_information(doc)
        self._db[collection].insert_many(docs, session=self._session)

    async def delete_one(self, collection: str, filter: Filter):
        """ "Delete the first document in `collection` matching `filter`."""
        self._add_current_block_to_filter(filter)
        self._db[collection].update_one(
            filter,
            {"$set": {"_chain.valid_to": self._block_number}},
            session=self._session,
        )

    async def delete_many(self, collection: str, filter: Filter):
        """Delete all documents in `collection` matching `filter`."""
        self._add_current_block_to_filter(filter)
        self._db[collection].update_many(
            filter,
            {"$set": {"_chain.valid_to": self._block_number}},
            session=self._session,
        )

    async def find_one(self, collection: str, filter: Filter) -> Optional[Document]:
        """Find the first document in `collection` matching `filter`."""
        self._add_current_block_to_filter(filter)
        return self._db[collection].find_one(filter, session=self._session)

    async def find(
        self,
        collection: str,
        filter: Filter,
        sort: Optional[dict[str, int]] = None,
        projection: Optional[Projection] = None,
        skip: int = 0,
        limit: int = 0,
    ) -> Iterable[dict]:
        """Find all documents in `collection` matching `filter`.

        Arguments
        ---------
        - `collection`: the collection,
        - `filter`: the filter,
        - `sort`: keys used for sorting, e.g. `{"a": -1}` sorts documents by key `a` in descending order,
        - `project`: filter document keys to reduce the document size,
        - `skip`: number of documents to skip,
        - `limit`: maximum number of documents returned.
        """
        self._add_current_block_to_filter(filter)
        cursor = self._db[collection].find(
            filter, projection, skip, limit, session=self._session
        )
        if sort is not None:
            for field, order in sort.items():
                cursor = cursor.sort(field, order)
        return cursor

    async def find_one_and_replace(
        self,
        collection: str,
        filter: Filter,
        replacement: Document,
        upsert: bool = False,
    ):
        """Replace the first document in `collection` matching `filter` with `replacement`.

        If `upsert = True`, insert `replacement` even if no document matched the `filter`.
        """
        # Step 1. Update the old document (if any) by clamping its validity range
        self._add_current_block_to_filter(filter)
        existing = self._db[collection].find_one_and_update(
            filter,
            {"$set": {"_chain.valid_to": self._block_number}},
            session=self._session,
        )

        # Step 2. Insert the new document.
        # Insert only if the existing document exists or if upsert.
        if existing is not None or upsert:
            await self.insert_one(collection, replacement)

        return existing

    async def find_one_and_update(
        self, collection: str, filter: Filter, update: Update
    ):
        """Update the first document in `collection` matching `filter` with `update`."""
        # Step 1. Update the old document (if any) by clamping its validity range
        self._add_current_block_to_filter(filter)
        existing = self._db[collection].find_one_and_update(
            filter,
            {"$set": {"_chain.valid_to": self._block_number}},
            session=self._session,
        )

        # Step 2. To simulate an update, first insert then call update on it.
        if existing is not None:
            del existing["_id"]
            del existing["_chain"]
            await self.insert_one(collection, existing)
            self._db[collection].update_one(filter, update, session=self._session)

        return existing

    def _add_chain_information(self, doc: Document):
        doc["_chain"] = {"valid_from": self._block_number, "valid_to": None}

    def _add_current_block_to_filter(self, filter: Filter):
        filter["_chain.valid_to"] = None
