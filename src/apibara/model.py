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
        hash = block.get("block_hash")
        if hash is not None:
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
        hash = "None"
        if self.hash is not None:
            hash = f"0x${self.hash.hex()}"
        return f"BlockHeader(hash={hash}, parent_hash=0x{self.parent_hash.hex()}, number={self.number}, timestamp={self.timestamp})"


@dataclass
class Event:
    """Base class for chain-specific events."""

    transaction: "Transaction"
    transaction_hash: bytes


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

    @classmethod
    def from_proto(cls, event, log_index, event_name, tx) -> "StarkNetEvent":
        address = base64.b64decode(event["from_address"]).ljust(32, b"\0")
        keys = [base64.b64decode(k).ljust(32, b"\0") for k in event["keys"]]
        data = [base64.b64decode(k).ljust(32, b"\0") for k in event["data"]]
        transaction = Transaction.from_proto(tx)
        return StarkNetEvent(
            name=event_name,
            address=address,
            log_index=log_index,
            topics=keys,
            data=data,
            transaction=transaction,
            transaction_hash=transaction.hash,
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


@dataclass
class Transaction:
    hash: bytes
    max_fee: Optional[bytes]
    signature: List[bytes]
    nonce: Optional[bytes]
    version: Optional[bytes]

    @classmethod
    def from_proto(cls, transaction) -> "Transaction":
        if transaction.get("invoke") is not None:
            return InvokeTransaction.from_proto(transaction["invoke"])
        if transaction.get("deploy") is not None:
            return DeployTransaction.from_proto(transaction["deploy"])
        if transaction.get("declare") is not None:
            return DeclareTransaction.from_proto(transaction["declare"])
        if transaction.get("l1_handler") is not None:
            return L1HandlerTransaction.from_proto(transaction["l1_handler"])
        if transaction.get("deploy_account") is not None:
            return DeployAccountTransaction.from_proto(transaction["deploy_account"])
        raise RuntimeError("invalid transaction type")


@dataclass
class InvokeTransaction(Transaction):
    contract_address: bytes
    entry_point_selector: bytes
    calldata: List[bytes]

    @classmethod
    def from_proto(cls, transaction) -> "Transaction":
        common = _common_attributes(transaction)
        callable = _callable_attributes(transaction)
        return InvokeTransaction(**common, **callable)


class DeployTransaction(Transaction):
    constructor_calldata: List[bytes]
    contract_address: bytes
    contract_address_salt: bytes
    class_hash: bytes

    @classmethod
    def from_proto(cls, transaction) -> "Transaction":
        raise RuntimeError("Deploy")
        pass


class DeclareTransaction(Transaction):
    class_hash: bytes
    sender_address: bytes

    @classmethod
    def from_proto(cls, transaction) -> "Transaction":
        raise RuntimeError("Declare")
        pass


@dataclass
class L1HandlerTransaction(Transaction):
    contract_address: bytes
    entry_point_selector: bytes
    calldata: List[bytes]

    @classmethod
    def from_proto(cls, transaction) -> "Transaction":
        common = _common_attributes(transaction)
        callable = _callable_attributes(transaction)
        return L1HandlerTransaction(**common, **callable)


class DeployAccountTransaction(Transaction):
    constructor_calldata: List[bytes]
    contract_address: bytes
    contract_address_salt: bytes
    class_hash: bytes

    @classmethod
    def from_proto(cls, transaction) -> "Transaction":
        raise RuntimeError("deploy account")
        pass


def _common_attributes(transaction):
    common = transaction["common"]
    hash = _from_base64_bytes(common["hash"], 32)
    max_fee = common.get("max_fee")
    if max_fee is not None:
        max_fee = _from_base64_bytes(max_fee)
    nonce = common.get("nonce")
    if nonce is not None:
        nonce = _from_base64_bytes(nonce)
    version = common.get("version")
    if version is not None:
        version = _from_base64_bytes(version)
    signature = [_from_base64_bytes(s) for s in common.get("signature", [])]
    return {
        "hash": hash,
        "max_fee": max_fee,
        "nonce": nonce,
        "version": version,
        "signature": signature,
    }


def _callable_attributes(transaction):
    contract_address = transaction.get("contract_address")
    if contract_address is not None:
        contract_address = _from_base64_bytes(contract_address, 32)
    entry_point_selector = transaction.get("entry_point_selector")
    if entry_point_selector is not None:
        entry_point_selector = _from_base64_bytes(entry_point_selector)
    calldata = [_from_base64_bytes(c) for c in transaction.get("calldata", [])]
    return {
        "contract_address": contract_address,
        "entry_point_selector": entry_point_selector,
        "calldata": calldata,
    }


def _from_base64_bytes(d: str, size: Optional[int] = None) -> bytes:
    if size is not None:
        return base64.b64decode(d).ljust(size, b"\0")
    return base64.b64decode(d)
