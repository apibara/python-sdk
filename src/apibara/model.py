"""Objects used in the Apibara client."""

import base64
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union


@dataclass(eq=True, frozen=True)
class EventFilter:
    """Filter transactions events based on their signature.
    
    The EventFilter can, optionally, filter by the emitting contract.
    
    Parameters
    ----------
    signature:
        the event signature.
    address:
        the contract address.
    """
    signature: str
    address: Optional[bytes]

    @classmethod
    def from_event_name(
        cls, name: str, address: Optional[Union[str, bytes, int]] = None
    ) -> "EventFilter":
        """Create an EventFilter from the event name and contract address."""
        if isinstance(address, str):
            address = bytes.fromhex(address.replace("0x", ""))
        if isinstance(address, int):
            address = address.to_bytes(32, "big")
        return cls(name, address)

    def to_json(self):
        """Returns the json representation of the filter."""
        return {"signature": self.signature, "address": self.address}

    @classmethod
    def from_json(cls, data):
        """Create an EventFilter from its json representation."""
        signature = data["signature"]
        if not isinstance(signature, str):
            raise ValueError("invalid signature. must be str")
        address = data.get("address")
        if address is None:
            return cls(signature, None)
        if not isinstance(address, bytes):
            raise ValueError("invalid address. must be bytes")
        return cls(signature, address)


@dataclass
class BlockHeader:
    """Information about a block.
    
    Parameters
    ----------
    hash:
        the block hash.
    parent_hash:
        the hash of the block's parent.
    number:
        the block number.
    timestamp:
        the block timestamp.
    """
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
    """Base class for chain-specific events."""
    pass


@dataclass
class StarkNetEvent(Event):
    """StarkNet event.
    
    Parameters
    ----------
    name:
        event name.
    address:
        address of the contract emitting the event.
    log_index:
        index in the list of events emitted by the block.
    topics:
        event topics. Usually this is the hash of the event name.
    data:
        raw event data.
    transaction_hash:
        hash of the transaction emitting the event.
    """
    name: Optional[str]
    address: bytes
    log_index: int
    topics: List[bytes]
    data: List[bytes]
    transaction_hash: bytes

    @classmethod
    def from_proto(cls, event, log_index, event_name, tx_hash) -> "StarkNetEvent":
        address = base64.b64decode(event["from_address"]).ljust(32, b"\0")
        keys = [base64.b64decode(k).ljust(32, b"\0") for k in event["keys"]]
        data = [base64.b64decode(k).ljust(32, b"\0") for k in event["data"]]
        return StarkNetEvent(
            name=event_name,
            address=address,
            log_index=log_index,
            topics=keys,
            data=data,
            transaction_hash=tx_hash,
        )


@dataclass
class NewBlock:
    """Information about a new block being indexed.
    
    Parameters
    ----------
    new_head:
        block header.
    """
    new_head: BlockHeader


@dataclass
class Reorg:
    new_head: BlockHeader


@dataclass
class NewEvents:
    """Information about indexed events in a block.
    
    Parameters
    ----------
    block
        the block containing the events.
    events:
        list of events.
    """
    block: BlockHeader
    events: List[Event]
