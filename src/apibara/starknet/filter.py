from typing import Any, List, Optional

import apibara.starknet.proto.filter_pb2 as proto
from apibara.starknet.proto.types_pb2 import FieldElement


class Filter:
    def __init__(self):
        self._inner = proto.Filter()

    def encode(self) -> bytes:
        return self._inner.SerializeToString()

    def to_proto(self) -> proto.Filter:
        return self._inner

    def parse(self, raw: bytes):
        self._inner.ParseFromString(raw)

    def merge(self, other: "Filter") -> "Filter":
        """
        Returns a new filter that will generate data for both filters.

        Parameters
        ----------
        other : Filter
            the other filter
        """
        new_filter = Filter()

        # decide wether to include headers or not
        has_header = False
        has_weak_header = False
        if self._inner.HasField("header"):
            has_header = True
            if self._inner.header.weak:
                has_weak_header = True
        if other._inner.HasField("header"):
            has_header = True
            if other._inner.header.weak:
                has_weak_header = True
        if has_header:
            new_filter.with_header(weak=has_weak_header)

        # concat all other filters.
        new_filter._inner.transactions.extend(self._inner.transactions)
        new_filter._inner.transactions.extend(other._inner.transactions)

        new_filter._inner.events.extend(self._inner.events)
        new_filter._inner.events.extend(other._inner.events)

        new_filter._inner.messages.extend(self._inner.messages)
        new_filter._inner.messages.extend(other._inner.messages)

        # merge state update filters
        if self._inner.HasField("state_update") or other._inner.HasField(
            "state_update"
        ):
            raise RuntimeError(
                "merging state updates is not supported yet. Please open an issue on github."
            )

        return new_filter

    def with_header(self, weak: Optional[bool] = None) -> "Filter":
        """
        Include header in the returned data.

        Parameters
        ----------
        weak : bool, optional
            if True, only include header if any other filter matches.
        """
        self._inner.header.CopyFrom(proto.HeaderFilter(weak=weak))
        return self

    def add_transaction(self, tx: "TransactionFilter") -> "Filter":
        """
        Include transaction data. Use an empty filter to return all transactions.
        """
        self._inner.transactions.extend([tx.encode()])
        return self

    def add_event(self, ev: "EventFilter") -> "Filter":
        """
        Include event data. Use an empty filter to include all events.
        """
        self._inner.events.extend([ev.encode()])
        return self

    def add_message(self, msg: "MessageFilter") -> "Filter":
        """
        Include messages from L2 to L1. Use an empty filter to include all messages.
        """
        self._inner.messages.extend([msg.encode()])
        return self

    def with_state_update(self, state_update: "StateUpdateFilter") -> "Filter":
        """
        Include state updates.
        """
        self._inner.state_update.CopyFrom(state_update.encode())
        return self


class TransactionFilter:
    @classmethod
    def any(cls) -> "TransactionFilter":
        """
        Include any transaction.
        """
        return TransactionFilter()

    @classmethod
    def invoke_v0(cls) -> "InvokeV0TransactionFilter":
        """
        Include invoke transactions, v0.
        """
        return InvokeV0TransactionFilter()

    @classmethod
    def invoke_v1(cls) -> "InvokeV1TransactionFilter":
        """
        Include invoke transactions, v1.
        """
        return InvokeV1TransactionFilter()

    @classmethod
    def deploy(cls) -> "DeployTransactionFilter":
        """
        Include deploy transactions.
        """
        return DeployTransactionFilter()

    @classmethod
    def declare(cls) -> "DeclareTransactionFilter":
        """
        Include declare transactions.
        """
        return DeclareTransactionFilter()

    @classmethod
    def l1_handler(cls) -> "L1HandlerTransactionFilter":
        """
        Include L1 handle transactions.
        """
        return L1HandlerTransactionFilter()

    @classmethod
    def deploy_account(cls) -> "DeployAccountTransactionFilter":
        """
        Include deploy account transactions.
        """
        return DeployAccountTransactionFilter()

    def encode(self) -> proto.TransactionFilter:
        return proto.TransactionFilter()


class InvokeV0TransactionFilter:
    def __init__(self) -> None:
        self._inner = proto.InvokeTransactionV0Filter()

    def with_contract_address(
        self, address: FieldElement
    ) -> "InvokeV0TransactionFilter":
        """
        Filter by contract address.
        """
        self._inner.contract_address.CopyFrom(address)
        return self

    def with_entry_point_selector(
        self, selector: FieldElement
    ) -> "InvokeV0TransactionFilter":
        """
        Filter by entry point selector.
        """
        self._inner.entry_point_selector.CopyFrom(selector)
        return self

    def with_calldata(
        self, calldata: List[FieldElement]
    ) -> "InvokeV0TransactionFilter":
        """
        Filter by calldata prefix.
        """
        del self._inner.calldata[:]
        self._inner.calldata.extend(calldata)
        return self

    def encode(self) -> proto.TransactionFilter:
        return proto.TransactionFilter(invoke_v0=self._inner)


class InvokeV1TransactionFilter:
    def __init__(self) -> None:
        self._inner = proto.InvokeTransactionV1Filter()

    def with_sender_address(self, address: FieldElement) -> "InvokeV1TransactionFilter":
        """
        Filter by sender address.
        """
        self._inner.sender_address.CopyFrom(address)
        return self

    def with_calldata(
        self, calldata: List[FieldElement]
    ) -> "InvokeV1TransactionFilter":
        """
        Filter by calldata prefix.
        """
        del self._inner.calldata[:]
        self._inner.calldata.extend(calldata)
        return self

    def encode(self) -> proto.TransactionFilter:
        return proto.TransactionFilter(invoke_v1=self._inner)


class DeployTransactionFilter:
    def __init__(self) -> None:
        self._inner = proto.DeployTransactionFilter()

    def with_contract_address_salt(
        self, address: FieldElement
    ) -> "DeployTransactionFilter":
        """
        Filter by contract address salt.
        """
        self._inner.contract_address_salt.CopyFrom(address)
        return self

    def with_class_hash(self, class_hash: FieldElement) -> "DeployTransactionFilter":
        """
        Filter by class hash.
        """
        self._inner.class_hash.CopyFrom(class_hash)
        return self

    def with_constructor_calldata(
        self, calldata: List[FieldElement]
    ) -> "DeployTransactionFilter":
        """
        Filter by constructor calldata prefix.
        """
        del self._inner.constructor_calldata[:]
        self._inner.constructor_calldata.extend(calldata)
        return self

    def encode(self) -> proto.TransactionFilter:
        return proto.TransactionFilter(deploy=self._inner)


class DeclareTransactionFilter:
    def __init__(self) -> None:
        self._inner = proto.DeclareTransactionFilter()

    def with_sender_address(self, address: FieldElement) -> "DeclareTransactionFilter":
        """
        Filter by sender address.
        """
        self._inner.sender_address.CopyFrom(address)
        return self

    def with_class_hash(self, class_hash: FieldElement) -> "DeclareTransactionFilter":
        """
        Filter by class hash.
        """
        self._inner.class_hash.CopyFrom(class_hash)
        return self

    def encode(self) -> proto.TransactionFilter:
        return proto.TransactionFilter(declare=self._inner)


class L1HandlerTransactionFilter:
    def __init__(self) -> None:
        self._inner = proto.L1HandlerTransactionFilter()

    def with_contract_address(
        self, address: FieldElement
    ) -> "L1HandlerTransactionFilter":
        """
        Filter by contract address.
        """
        self._inner.contract_address.CopyFrom(address)
        return self

    def with_entry_point_selector(
        self, selector: FieldElement
    ) -> "L1HandlerTransactionFilter":
        """
        Filter by entry point selector.
        """
        self._inner.entry_point_selector.CopyFrom(selector)
        return self

    def with_calldata(
        self, calldata: List[FieldElement]
    ) -> "L1HandlerTransactionFilter":
        """
        Filter by calldata prefix.
        """
        del self._inner.calldata[:]
        self._inner.calldata.extend(calldata)
        return self

    def encode(self) -> proto.TransactionFilter:
        return proto.TransactionFilter(l1_handler=self._inner)


class DeployAccountTransactionFilter:
    def __init__(self) -> None:
        self._inner = proto.DeployAccountTransactionFilter()

    def with_contract_address_salt(
        self, address: FieldElement
    ) -> "DeployAccountTransactionFilter":
        """
        Filter by contract address salt.
        """
        self._inner.contract_address_salt.CopyFrom(address)
        return self

    def with_class_hash(
        self, class_hash: FieldElement
    ) -> "DeployAccountTransactionFilter":
        """
        Filter by class hash.
        """
        self._inner.class_hash.CopyFrom(class_hash)
        return self

    def with_constructor_calldata(
        self, calldata: List[FieldElement]
    ) -> "DeployAccountTransactionFilter":
        """
        Filter by constructor calldata prefix.
        """
        del self._inner.constructor_calldata[:]
        self._inner.constructor_calldata.extend(calldata)
        return self

    def encode(self) -> proto.TransactionFilter:
        return proto.TransactionFilter(deploy_account=self._inner)


class EventFilter:
    def __init__(self):
        self._inner = proto.EventFilter()

    def with_from_address(self, address: FieldElement) -> "EventFilter":
        """
        Filter by address of the contract emitting the event.
        """
        self._inner.from_address.CopyFrom(address)
        return self

    def with_keys(self, keys: List[FieldElement]) -> "EventFilter":
        """
        Filter by keys prefix.
        """
        del self._inner.keys[:]
        self._inner.keys.extend(keys)
        return self

    def with_data(self, data: List[FieldElement]) -> "EventFilter":
        """
        Filter by data prefix.
        """
        del self._inner.data[:]
        self._inner.data.extend(data)
        return self

    def encode(self) -> proto.EventFilter:
        return self._inner


class MessageFilter:
    def __init__(self) -> None:
        self._inner = proto.L2ToL1MessageFilter()

    def with_to_address(self, address: FieldElement) -> "MessageFilter":
        """
        Filter by address.
        """
        self._inner.to_address.CopyFrom(address)
        return self

    def with_payload(self, payload: List[FieldElement]) -> "MessageFilter":
        """
        Filter by payload prefix.
        """
        del self._inner.payload[:]
        self._inner.payload.extend(payload)
        return self

    def encode(self) -> proto.L2ToL1MessageFilter:
        return self._inner


class StateUpdateFilter:
    def __init__(self):
        self._inner = proto.StateUpdateFilter()

    def add_storage_diff(self, diff: "StorageDiffFilter") -> "StateUpdateFilter":
        """
        Includes all storage changes that match the filter.
        """
        self._inner.storage_diffs.extend([diff.encode()])
        return self

    def add_declared_contract(
        self, decl: "DeclaredContractFilter"
    ) -> "StateUpdateFilter":
        """
        Includes all declared contracts that match the filter.
        """
        self._inner.declared_contracts.extend([decl.encode()])
        return self

    def add_deployed_contract(
        self, deploy: "DeployedContractFilter"
    ) -> "StateUpdateFilter":
        """
        Includes all deployed contracts that match the filter.
        """
        self._inner.deployed_contracts.extend([deploy.encode()])
        return self

    def add_nonce_update(self, update: "NonceUpdateFilter") -> "StateUpdateFilter":
        """
        Includes all nonce updates that match the filter.
        """
        self._inner.nonces.extend([update.encode()])
        return self

    def encode(self) -> proto.StateUpdateFilter:
        return self._inner


class StorageDiffFilter:
    def __init__(self):
        self._inner = proto.StorageDiffFilter()

    def with_contract_address(self, address: FieldElement) -> "StorageDiffFilter":
        """
        Filter by contract address.
        """
        self._inner.contract_address.CopyFrom(address)
        return self

    def encode(self) -> proto.StorageDiffFilter:
        return self._inner


class DeclaredContractFilter:
    def __init__(self):
        self._inner = proto.DeclaredContractFilter()

    def with_class_hash(self, class_hash: FieldElement) -> "DeclaredContractFilter":
        """
        Filter by class hash.
        """
        self._inner.class_hash.CopyFrom(class_hash)
        return self

    def encode(self) -> proto.DeclaredContractFilter:
        return self._inner


class DeployedContractFilter:
    def __init__(self):
        self._inner = proto.DeployedContractFilter()

    def with_contract_address(self, address: FieldElement) -> "DeployedContractFilter":
        """
        Filter by contract address.
        """
        self._inner.contract_address.CopyFrom(address)
        return self

    def with_class_hash(self, class_hash: FieldElement) -> "DeployedContractFilter":
        """
        Filter by class hash.
        """
        self._inner.class_hash.CopyFrom(class_hash)
        return self

    def encode(self) -> proto.DeployedContractFilter:
        return self._inner


class NonceUpdateFilter:
    def __init__(self):
        self._inner = proto.NonceUpdateFilter()

    def with_contract_address(self, address: FieldElement) -> "NonceUpdateFilter":
        """
        Filter by contract address.
        """
        self._inner.contract_address.CopyFrom(address)
        return self

    def with_nonce(self, nonce: FieldElement) -> "NonceUpdateFilter":
        """
        Filter by nonce.
        """
        self._inner.nonce.CopyFrom(nonce)
        return self

    def encode(self) -> proto.NonceUpdateFilter:
        return self._inner
