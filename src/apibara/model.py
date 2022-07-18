"""Objects used in the Apibara client."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal, Optional, Union

import apibara.application.indexer_service_pb2 as indexer_service_pb2
from apibara.starknet import get_selector_from_name


@dataclass
class EventFilter:
    signature: str
    address: Optional[bytes]

    @classmethod
    def from_event_name(
        cls, name: str, address: Optional[Union[str, bytes]]
    ) -> "EventFilter":
        """Create an EventFilter from the event name."""
        if isinstance(address, str):
            address = bytes.fromhex(address.replace("0x", ""))
        return cls(name, address)

    @staticmethod
    def from_proto(p: indexer_service_pb2.EventFilter):
        address = None
        if len(p.address) > 0:
            address = p.address
        return EventFilter(signature=p.signature, address=address)

    def to_proto(self) -> indexer_service_pb2.EventFilter:
        return indexer_service_pb2.EventFilter(
            signature=self.signature,
            address=self.address,
        )

    def __str__(self) -> str:
        address = ""
        if self.address is not None:
            address = f", address=0x{self.address.hex()}"
        return f"EventFilter(signature={self.signature}{address})"


@dataclass
class Network:
    name: str
    type: Literal["evm", "starknet"]

    @staticmethod
    def from_proto(p: indexer_service_pb2.Network):
        if p.HasField("starknet"):
            return Network(p.starknet.name, "starknet")
        if p.HasField("ethereum"):
            return Network(p.ethereum.name, "evm")
        raise ValueError("invalid network proto object")

    def __str__(self) -> str:
        return f"Network(name={self.name}, type={self.type})"


@dataclass
class Indexer:
    id: str
    index_from_block: int
    indexed_to_block: int
    filters: List[EventFilter]
    network: Network

    @staticmethod
    def from_proto(p: indexer_service_pb2.Indexer):
        filters = [EventFilter.from_proto(f) for f in p.filters]
        network = Network.from_proto(p.network)
        return Indexer(p.id, p.index_from_block, p.indexed_to_block, filters, network)

    def __str__(self) -> str:
        return f'Indexer(id={self.id}, network={self.network}, blocks=[{self.index_from_block}, {self.indexed_to_block}], filters=[{", ".join(str(f) for f in self.filters)}])'


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    @staticmethod
    def from_proto(p: indexer_service_pb2.Version):
        return Version(major=p.major, minor=p.minor, patch=p.patch)


@dataclass
class IndexerConnected:
    indexer: Indexer
    version: Version

    @staticmethod
    def from_proto(p: indexer_service_pb2.IndexerConnected):
        indexer = Indexer.from_proto(p.indexer)
        version = Version.from_proto(p.version)
        return IndexerConnected(indexer=indexer, version=version)


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
    @staticmethod
    def from_proto(p: indexer_service_pb2.Event):
        if p.HasField("starknet"):
            return StarkNetEvent.from_proto(p.starknet)
        if p.HasField("ethereum"):
            return EthereumEvent.from_proto(p.ethereum)


@dataclass
class StarkNetEvent(Event):
    name: Optional[str]
    address: bytes
    log_index: int
    topics: List[bytes]
    data: List[bytes]

    @staticmethod
    def from_proto(p: indexer_service_pb2.StarkNetEvent):
        topics = [bytes(t.value) for t in p.topics]
        data = [bytes(d.value) for d in p.data]
        return StarkNetEvent(
            name=None,
            address=bytes(p.address),
            log_index=p.log_index,
            topics=topics,
            data=data,
        )

    def __str__(self) -> str:
        name = ""
        if self.name is not None:
            name = f"name={self.name}, "
        return f"StarkNetEvent({name}address=0x{self.address.hex()}, log_index={self.log_index}, ...{len(self.topics)} topics, ...{len(self.data)} data)"


@dataclass
class EthereumEvent(Event):
    name: Optional[str]
    address: bytes
    log_index: int
    topics: List[bytes]
    data: bytes

    @staticmethod
    def from_proto(p: indexer_service_pb2.EthereumEvent):
        topics = [bytes(t.value) for t in p.topics]
        return EthereumEvent(
            name=None,
            address=bytes(p.address),
            log_index=p.log_index,
            topics=topics,
            data=p.data,
        )

    def __str__(self) -> str:
        name = ""
        if self.name is not None:
            name = f"name={self.name}, "
        return f"EthereumEvent({name}address=0x{self.address.hex()}, log_index={self.log_index}, ...{len(self.topics)} topics, ...{len(self.data)} data)"


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
    block: BlockHeader
    events: List[Event]

    @staticmethod
    def from_proto(p: indexer_service_pb2.NewEvents):
        block = BlockHeader.from_proto(p.block)
        events = [Event.from_proto(ev) for ev in p.events]
        return NewEvents(block, events)

    def __str__(self) -> str:
        return f"NewEvents(block={self.block}, ...{len(self.events)} events)"
