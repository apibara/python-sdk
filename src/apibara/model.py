"""Objects used in the Apibara client."""

import base64
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union


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


@dataclass
class BlockHeader:
    hash: bytes
    parent_hash: Optional[bytes]
    number: int
    timestamp: datetime

    @classmethod
    def from_proto(cls, block) -> "BlockHeader":
        hash = base64.b64decode(block["block_hash"]["hash"]).ljust(32, b"\0")
        parent_hash = base64.b64decode(block["parent_block_hash"]["hash"]).ljust(
            32, b"\0"
        )
        number = int(block.get("block_number", 0))
        timestamp = datetime.fromisoformat(block["timestamp"][:-1])
        return BlockHeader(
            hash=hash, parent_hash=parent_hash, number=number, timestamp=timestamp
        )

    def __str__(self) -> str:
        return f"BlockHeader(hash=0x{self.hash.hex()}, parent_hash=0x{self.parent_hash.hex()}, number={self.number}, timestamp={self.timestamp})"


@dataclass
class Event:
    pass


@dataclass
class StarkNetEvent(Event):
    name: Optional[str]
    address: bytes
    log_index: int
    topics: List[bytes]
    data: List[bytes]
    transaction_hash: bytes

    @classmethod
    def from_proto(cls, event, log_index, event_name) -> "StarkNetEvent":
        address = base64.b64decode(event["from_address"]).ljust(32, b"\0")
        keys = [base64.b64decode(k).ljust(32, b"\0") for k in event["keys"]]
        data = [base64.b64decode(k).ljust(32, b"\0") for k in event["data"]]
        return StarkNetEvent(
            name=event_name,
            address=address,
            log_index=log_index,
            topics=keys,
            data=data,
            transaction_hash=None,
        )


@dataclass
class NewBlock:
    new_head: BlockHeader


@dataclass
class Reorg:
    new_head: BlockHeader


@dataclass
class NewEvents:
    block: BlockHeader
    events: List[Event]
