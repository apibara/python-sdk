from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

import apibara.starknet.proto.types_pb2 as _types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class BlockStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    BLOCK_STATUS_UNSPECIFIED: _ClassVar[BlockStatus]
    BLOCK_STATUS_PENDING: _ClassVar[BlockStatus]
    BLOCK_STATUS_ACCEPTED_ON_L2: _ClassVar[BlockStatus]
    BLOCK_STATUS_ACCEPTED_ON_L1: _ClassVar[BlockStatus]
    BLOCK_STATUS_REJECTED: _ClassVar[BlockStatus]

BLOCK_STATUS_UNSPECIFIED: BlockStatus
BLOCK_STATUS_PENDING: BlockStatus
BLOCK_STATUS_ACCEPTED_ON_L2: BlockStatus
BLOCK_STATUS_ACCEPTED_ON_L1: BlockStatus
BLOCK_STATUS_REJECTED: BlockStatus

class Block(_message.Message):
    __slots__ = [
        "status",
        "header",
        "transactions",
        "state_update",
        "events",
        "l2_to_l1_messages",
    ]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    STATE_UPDATE_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    L2_TO_L1_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    status: BlockStatus
    header: BlockHeader
    transactions: _containers.RepeatedCompositeFieldContainer[TransactionWithReceipt]
    state_update: StateUpdate
    events: _containers.RepeatedCompositeFieldContainer[EventWithTransaction]
    l2_to_l1_messages: _containers.RepeatedCompositeFieldContainer[
        L2ToL1MessageWithTransaction
    ]
    def __init__(
        self,
        status: _Optional[_Union[BlockStatus, str]] = ...,
        header: _Optional[_Union[BlockHeader, _Mapping]] = ...,
        transactions: _Optional[
            _Iterable[_Union[TransactionWithReceipt, _Mapping]]
        ] = ...,
        state_update: _Optional[_Union[StateUpdate, _Mapping]] = ...,
        events: _Optional[_Iterable[_Union[EventWithTransaction, _Mapping]]] = ...,
        l2_to_l1_messages: _Optional[
            _Iterable[_Union[L2ToL1MessageWithTransaction, _Mapping]]
        ] = ...,
    ) -> None: ...

class BlockHeader(_message.Message):
    __slots__ = [
        "block_hash",
        "parent_block_hash",
        "block_number",
        "sequencer_address",
        "new_root",
        "timestamp",
    ]
    BLOCK_HASH_FIELD_NUMBER: _ClassVar[int]
    PARENT_BLOCK_HASH_FIELD_NUMBER: _ClassVar[int]
    BLOCK_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SEQUENCER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NEW_ROOT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    block_hash: _types_pb2.FieldElement
    parent_block_hash: _types_pb2.FieldElement
    block_number: int
    sequencer_address: _types_pb2.FieldElement
    new_root: _types_pb2.FieldElement
    timestamp: _timestamp_pb2.Timestamp
    def __init__(
        self,
        block_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        parent_block_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        block_number: _Optional[int] = ...,
        sequencer_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        new_root: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class TransactionWithReceipt(_message.Message):
    __slots__ = ["transaction", "receipt"]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_FIELD_NUMBER: _ClassVar[int]
    transaction: Transaction
    receipt: TransactionReceipt
    def __init__(
        self,
        transaction: _Optional[_Union[Transaction, _Mapping]] = ...,
        receipt: _Optional[_Union[TransactionReceipt, _Mapping]] = ...,
    ) -> None: ...

class Transaction(_message.Message):
    __slots__ = [
        "meta",
        "invoke_v0",
        "invoke_v1",
        "deploy",
        "declare",
        "l1_handler",
        "deploy_account",
    ]
    META_FIELD_NUMBER: _ClassVar[int]
    INVOKE_V0_FIELD_NUMBER: _ClassVar[int]
    INVOKE_V1_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_FIELD_NUMBER: _ClassVar[int]
    DECLARE_FIELD_NUMBER: _ClassVar[int]
    L1_HANDLER_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    meta: TransactionMeta
    invoke_v0: InvokeTransactionV0
    invoke_v1: InvokeTransactionV1
    deploy: DeployTransaction
    declare: DeclareTransaction
    l1_handler: L1HandlerTransaction
    deploy_account: DeployAccountTransaction
    def __init__(
        self,
        meta: _Optional[_Union[TransactionMeta, _Mapping]] = ...,
        invoke_v0: _Optional[_Union[InvokeTransactionV0, _Mapping]] = ...,
        invoke_v1: _Optional[_Union[InvokeTransactionV1, _Mapping]] = ...,
        deploy: _Optional[_Union[DeployTransaction, _Mapping]] = ...,
        declare: _Optional[_Union[DeclareTransaction, _Mapping]] = ...,
        l1_handler: _Optional[_Union[L1HandlerTransaction, _Mapping]] = ...,
        deploy_account: _Optional[_Union[DeployAccountTransaction, _Mapping]] = ...,
    ) -> None: ...

class TransactionMeta(_message.Message):
    __slots__ = ["hash", "max_fee", "signature", "nonce", "version"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    MAX_FEE_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    hash: _types_pb2.FieldElement
    max_fee: _types_pb2.FieldElement
    signature: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    nonce: _types_pb2.FieldElement
    version: int
    def __init__(
        self,
        hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        max_fee: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        signature: _Optional[
            _Iterable[_Union[_types_pb2.FieldElement, _Mapping]]
        ] = ...,
        nonce: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        version: _Optional[int] = ...,
    ) -> None: ...

class InvokeTransactionV0(_message.Message):
    __slots__ = ["contract_address", "entry_point_selector", "calldata"]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ENTRY_POINT_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    CALLDATA_FIELD_NUMBER: _ClassVar[int]
    contract_address: _types_pb2.FieldElement
    entry_point_selector: _types_pb2.FieldElement
    calldata: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        entry_point_selector: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        calldata: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
    ) -> None: ...

class InvokeTransactionV1(_message.Message):
    __slots__ = ["sender_address", "calldata"]
    SENDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CALLDATA_FIELD_NUMBER: _ClassVar[int]
    sender_address: _types_pb2.FieldElement
    calldata: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    def __init__(
        self,
        sender_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        calldata: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
    ) -> None: ...

class DeployTransaction(_message.Message):
    __slots__ = ["constructor_calldata", "contract_address_salt", "class_hash"]
    CONSTRUCTOR_CALLDATA_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_SALT_FIELD_NUMBER: _ClassVar[int]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    constructor_calldata: _containers.RepeatedCompositeFieldContainer[
        _types_pb2.FieldElement
    ]
    contract_address_salt: _types_pb2.FieldElement
    class_hash: _types_pb2.FieldElement
    def __init__(
        self,
        constructor_calldata: _Optional[
            _Iterable[_Union[_types_pb2.FieldElement, _Mapping]]
        ] = ...,
        contract_address_salt: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class DeclareTransaction(_message.Message):
    __slots__ = ["class_hash", "sender_address", "compiled_class_hash"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    SENDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COMPILED_CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    sender_address: _types_pb2.FieldElement
    compiled_class_hash: _types_pb2.FieldElement
    def __init__(
        self,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        sender_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        compiled_class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class L1HandlerTransaction(_message.Message):
    __slots__ = ["contract_address", "entry_point_selector", "calldata"]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ENTRY_POINT_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    CALLDATA_FIELD_NUMBER: _ClassVar[int]
    contract_address: _types_pb2.FieldElement
    entry_point_selector: _types_pb2.FieldElement
    calldata: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        entry_point_selector: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        calldata: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
    ) -> None: ...

class DeployAccountTransaction(_message.Message):
    __slots__ = ["constructor_calldata", "contract_address_salt", "class_hash"]
    CONSTRUCTOR_CALLDATA_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_SALT_FIELD_NUMBER: _ClassVar[int]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    constructor_calldata: _containers.RepeatedCompositeFieldContainer[
        _types_pb2.FieldElement
    ]
    contract_address_salt: _types_pb2.FieldElement
    class_hash: _types_pb2.FieldElement
    def __init__(
        self,
        constructor_calldata: _Optional[
            _Iterable[_Union[_types_pb2.FieldElement, _Mapping]]
        ] = ...,
        contract_address_salt: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class TransactionReceipt(_message.Message):
    __slots__ = [
        "transaction_hash",
        "transaction_index",
        "actual_fee",
        "l2_to_l1_messages",
        "events",
        "contract_address",
    ]
    TRANSACTION_HASH_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_INDEX_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_FEE_FIELD_NUMBER: _ClassVar[int]
    L2_TO_L1_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    transaction_hash: _types_pb2.FieldElement
    transaction_index: int
    actual_fee: _types_pb2.FieldElement
    l2_to_l1_messages: _containers.RepeatedCompositeFieldContainer[L2ToL1Message]
    events: _containers.RepeatedCompositeFieldContainer[Event]
    contract_address: _types_pb2.FieldElement
    def __init__(
        self,
        transaction_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        transaction_index: _Optional[int] = ...,
        actual_fee: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        l2_to_l1_messages: _Optional[_Iterable[_Union[L2ToL1Message, _Mapping]]] = ...,
        events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class L2ToL1MessageWithTransaction(_message.Message):
    __slots__ = ["transaction", "receipt", "message"]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    transaction: Transaction
    receipt: TransactionReceipt
    message: L2ToL1Message
    def __init__(
        self,
        transaction: _Optional[_Union[Transaction, _Mapping]] = ...,
        receipt: _Optional[_Union[TransactionReceipt, _Mapping]] = ...,
        message: _Optional[_Union[L2ToL1Message, _Mapping]] = ...,
    ) -> None: ...

class L2ToL1Message(_message.Message):
    __slots__ = ["to_address", "payload", "index", "from_address"]
    TO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    to_address: _types_pb2.FieldElement
    payload: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    index: int
    from_address: _types_pb2.FieldElement
    def __init__(
        self,
        to_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        payload: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        index: _Optional[int] = ...,
        from_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class EventWithTransaction(_message.Message):
    __slots__ = ["transaction", "receipt", "event"]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    transaction: Transaction
    receipt: TransactionReceipt
    event: Event
    def __init__(
        self,
        transaction: _Optional[_Union[Transaction, _Mapping]] = ...,
        receipt: _Optional[_Union[TransactionReceipt, _Mapping]] = ...,
        event: _Optional[_Union[Event, _Mapping]] = ...,
    ) -> None: ...

class Event(_message.Message):
    __slots__ = ["from_address", "keys", "data", "index"]
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    from_address: _types_pb2.FieldElement
    keys: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    data: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    index: int
    def __init__(
        self,
        from_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        keys: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        data: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        index: _Optional[int] = ...,
    ) -> None: ...

class StateUpdate(_message.Message):
    __slots__ = ["new_root", "old_root", "state_diff"]
    NEW_ROOT_FIELD_NUMBER: _ClassVar[int]
    OLD_ROOT_FIELD_NUMBER: _ClassVar[int]
    STATE_DIFF_FIELD_NUMBER: _ClassVar[int]
    new_root: _types_pb2.FieldElement
    old_root: _types_pb2.FieldElement
    state_diff: StateDiff
    def __init__(
        self,
        new_root: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        old_root: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        state_diff: _Optional[_Union[StateDiff, _Mapping]] = ...,
    ) -> None: ...

class StateDiff(_message.Message):
    __slots__ = [
        "storage_diffs",
        "declared_contracts",
        "deployed_contracts",
        "nonces",
        "declared_classes",
        "replaced_classes",
    ]
    STORAGE_DIFFS_FIELD_NUMBER: _ClassVar[int]
    DECLARED_CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYED_CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    NONCES_FIELD_NUMBER: _ClassVar[int]
    DECLARED_CLASSES_FIELD_NUMBER: _ClassVar[int]
    REPLACED_CLASSES_FIELD_NUMBER: _ClassVar[int]
    storage_diffs: _containers.RepeatedCompositeFieldContainer[StorageDiff]
    declared_contracts: _containers.RepeatedCompositeFieldContainer[DeclaredContract]
    deployed_contracts: _containers.RepeatedCompositeFieldContainer[DeployedContract]
    nonces: _containers.RepeatedCompositeFieldContainer[NonceUpdate]
    declared_classes: _containers.RepeatedCompositeFieldContainer[DeclaredClass]
    replaced_classes: _containers.RepeatedCompositeFieldContainer[ReplacedClass]
    def __init__(
        self,
        storage_diffs: _Optional[_Iterable[_Union[StorageDiff, _Mapping]]] = ...,
        declared_contracts: _Optional[
            _Iterable[_Union[DeclaredContract, _Mapping]]
        ] = ...,
        deployed_contracts: _Optional[
            _Iterable[_Union[DeployedContract, _Mapping]]
        ] = ...,
        nonces: _Optional[_Iterable[_Union[NonceUpdate, _Mapping]]] = ...,
        declared_classes: _Optional[_Iterable[_Union[DeclaredClass, _Mapping]]] = ...,
        replaced_classes: _Optional[_Iterable[_Union[ReplacedClass, _Mapping]]] = ...,
    ) -> None: ...

class StorageDiff(_message.Message):
    __slots__ = ["contract_address", "storage_entries"]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    contract_address: _types_pb2.FieldElement
    storage_entries: _containers.RepeatedCompositeFieldContainer[StorageEntry]
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        storage_entries: _Optional[_Iterable[_Union[StorageEntry, _Mapping]]] = ...,
    ) -> None: ...

class StorageEntry(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: _types_pb2.FieldElement
    value: _types_pb2.FieldElement
    def __init__(
        self,
        key: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        value: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class DeclaredContract(_message.Message):
    __slots__ = ["class_hash"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    def __init__(
        self, class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...
    ) -> None: ...

class DeclaredClass(_message.Message):
    __slots__ = ["class_hash", "compiled_class_hash"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    COMPILED_CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    compiled_class_hash: _types_pb2.FieldElement
    def __init__(
        self,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        compiled_class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class ReplacedClass(_message.Message):
    __slots__ = ["contract_address", "class_hash"]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    contract_address: _types_pb2.FieldElement
    class_hash: _types_pb2.FieldElement
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class DeployedContract(_message.Message):
    __slots__ = ["contract_address", "class_hash"]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    contract_address: _types_pb2.FieldElement
    class_hash: _types_pb2.FieldElement
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class NonceUpdate(_message.Message):
    __slots__ = ["contract_address", "nonce"]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    contract_address: _types_pb2.FieldElement
    nonce: _types_pb2.FieldElement
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        nonce: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...
