"""Objects used in the Apibara client."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

import apibara.application.indexer_service_pb2 as indexer_service_pb2
from apibara.starknet import get_selector_from_name


@dataclass
class Topic:
    choices: List[bytes]

    @staticmethod
    def from_proto(p: indexer_service_pb2.Topic):
        return Topic([c.value for c in p.choices])

    def to_proto(self) -> indexer_service_pb2.Topic:
        return indexer_service_pb2.Topic(
            choices=[indexer_service_pb2.TopicValue(value=c) for c in self.choices]
        )

    def __str__(self) -> str:
        choices = [f"0x{c.hex()}" for c in self.choices]
        return f'Topic({"|".join(choices)})'


@dataclass
class EventFilter:
    name: Optional[str]
    address: Optional[bytes]
    topics: List[Topic]

    @classmethod
    def from_event_name(
        cls, name: str, address: Optional[Union[str, bytes]]
    ) -> "EventFilter":
        """Create an EventFilter from the event name."""
        if isinstance(address, str):
            address = bytes.fromhex(address.replace("0x", ""))
        topic_hex = hex(get_selector_from_name(name))[2:]
        # fromhex requires an even number of digits
        if len(topic_hex) % 2 == 1:
            topic_hex = "0" + topic_hex
        topic_value = bytes.fromhex(topic_hex)
        topics = [Topic([topic_value])]

        return cls(name, address, topics)

    @staticmethod
    def from_proto(p: indexer_service_pb2.EventFilter):
        address = None
        if len(p.address) > 0:
            address = p.address

        topics = [Topic.from_proto(t) for t in p.topics]
        return EventFilter(name=None, address=address, topics=topics)

    def to_proto(self) -> indexer_service_pb2.EventFilter:
        return indexer_service_pb2.EventFilter(
            address=self.address, topics=[t.to_proto() for t in self.topics]
        )

    def __str__(self) -> str:
        address = ""
        if self.address is not None:
            address = f"address=0x{self.address.hex()}, "
        return (
            f'EventFilter({address}topics=[{", ".join(str(t) for t in self.topics)}])'
        )


@dataclass
class Indexer:
    id: str
    index_from_block: int
    indexed_to_block: int
    filters: List[EventFilter]

    @staticmethod
    def from_proto(p: indexer_service_pb2.Indexer):
        filters = [EventFilter.from_proto(f) for f in p.filters]
        return Indexer(p.id, p.index_from_block, p.indexed_to_block, filters)

    def __str__(self) -> str:
        return f'Indexer(id={self.id}, blocks=[{self.index_from_block}, {self.indexed_to_block}], filters=[{", ".join(str(f) for f in self.filters)}])'


@dataclass
class IndexerConnected:
    indexer: Indexer

    @staticmethod
    def from_proto(p: indexer_service_pb2.IndexerConnected):
        app = Indexer.from_proto(p.indexer)
        return IndexerConnected(app)


@dataclass
class BlockHeader:
    hash: bytes
    parent_hash: Optional[bytes]
    number: int
    timestamp: datetime

    @staticmethod
    def from_proto(p: indexer_service_pb2.BlockHeader):
        dt = datetime.fromtimestamp(p.timestamp.seconds)
        return BlockHeader(bytes(p.hash), bytes(p.parent_hash), p.number, dt)

    def __str__(self) -> str:
        return f"BlockHeader(hash=0x{self.hash.hex()}, parent_hash=0x{self.parent_hash.hex()}, number={self.number}, timestamp={self.timestamp})"


@dataclass
class Event:
    name: Optional[str]
    address: bytes
    block_index: int
    topics: List[bytes]
    data: List[bytes]

    @staticmethod
    def from_proto(p: indexer_service_pb2.Event):
        topics = [bytes(t.value) for t in p.topics]
        data = [bytes(d.value) for d in p.data]
        return Event(None, bytes(p.address), p.block_index, topics, data)

    def __str__(self) -> str:
        name = ""
        if self.name is not None:
            name = f"name={self.name}, "
        return f"Event({name}address=0x{self.address.hex()}, block_index={self.block_index}, ...{len(self.topics)} topics, ...{len(self.data)} data)"


@dataclass
class NewBlock:
    new_head: BlockHeader

    @staticmethod
    def from_proto(p: indexer_service_pb2.NewBlock):
        new_head = BlockHeader.from_proto(p.new_head)
        return NewBlock(new_head)

    def __str__(self) -> str:
        return f"NewBlock(new_head={self.new_head})"


@dataclass
class Reorg:
    new_head: BlockHeader

    @staticmethod
    def from_proto(p: indexer_service_pb2.Reorg):
        new_head = BlockHeader.from_proto(p.new_head)
        return Reorg(new_head)

    def __str__(self) -> str:
        return f"Reorg(new_head={self.new_head})"


@dataclass
class NewEvents:
    block_hash: bytes
    block_number: int
    events: List[Event]

    @staticmethod
    def from_proto(p: indexer_service_pb2.NewEvents):
        events = [Event.from_proto(ev) for ev in p.events]
        return NewEvents(bytes(p.block_hash), p.block_number, events)

    def __str__(self) -> str:
        return f"NewEvents(block_hash=0x{self.block_hash.hex()}, block_number={self.block_number}, ...{len(self.events)} events)"
