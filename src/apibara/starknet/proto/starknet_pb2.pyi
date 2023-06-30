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

BLOCK_STATUS_ACCEPTED_ON_L1: BlockStatus
BLOCK_STATUS_ACCEPTED_ON_L2: BlockStatus
BLOCK_STATUS_PENDING: BlockStatus
BLOCK_STATUS_REJECTED: BlockStatus
BLOCK_STATUS_UNSPECIFIED: BlockStatus
DESCRIPTOR: _descriptor.FileDescriptor

class Block(_message.Message):
    __slots__ = [
        "events",
        "header",
        "l2_to_l1_messages",
        "state_update",
        "status",
        "transactions",
    ]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    L2_TO_L1_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    STATE_UPDATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[EventWithTransaction]
    header: BlockHeader
    l2_to_l1_messages: _containers.RepeatedCompositeFieldContainer[
        L2ToL1MessageWithTransaction
    ]
    state_update: StateUpdate
    status: BlockStatus
    transactions: _containers.RepeatedCompositeFieldContainer[TransactionWithReceipt]
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
        "block_number",
        "new_root",
        "parent_block_hash",
        "sequencer_address",
        "timestamp",
    ]
    BLOCK_HASH_FIELD_NUMBER: _ClassVar[int]
    BLOCK_NUMBER_FIELD_NUMBER: _ClassVar[int]
    NEW_ROOT_FIELD_NUMBER: _ClassVar[int]
    PARENT_BLOCK_HASH_FIELD_NUMBER: _ClassVar[int]
    SEQUENCER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    block_hash: _types_pb2.FieldElement
    block_number: int
    new_root: _types_pb2.FieldElement
    parent_block_hash: _types_pb2.FieldElement
    sequencer_address: _types_pb2.FieldElement
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

class DeclareTransaction(_message.Message):
    __slots__ = ["class_hash", "compiled_class_hash", "sender_address"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    COMPILED_CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    SENDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    compiled_class_hash: _types_pb2.FieldElement
    sender_address: _types_pb2.FieldElement
    def __init__(
        self,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        sender_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        compiled_class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
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

class DeclaredContract(_message.Message):
    __slots__ = ["class_hash"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    def __init__(
        self, class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...
    ) -> None: ...

class DeployAccountTransaction(_message.Message):
    __slots__ = ["class_hash", "constructor_calldata", "contract_address_salt"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    CONSTRUCTOR_CALLDATA_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_SALT_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    constructor_calldata: _containers.RepeatedCompositeFieldContainer[
        _types_pb2.FieldElement
    ]
    contract_address_salt: _types_pb2.FieldElement
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

class DeployTransaction(_message.Message):
    __slots__ = ["class_hash", "constructor_calldata", "contract_address_salt"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    CONSTRUCTOR_CALLDATA_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_SALT_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    constructor_calldata: _containers.RepeatedCompositeFieldContainer[
        _types_pb2.FieldElement
    ]
    contract_address_salt: _types_pb2.FieldElement
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

class DeployedContract(_message.Message):
    __slots__ = ["class_hash", "contract_address"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    contract_address: _types_pb2.FieldElement
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class Event(_message.Message):
    __slots__ = ["data", "from_address", "index", "keys"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    from_address: _types_pb2.FieldElement
    index: int
    keys: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    def __init__(
        self,
        from_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        keys: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        data: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        index: _Optional[int] = ...,
    ) -> None: ...

class EventWithTransaction(_message.Message):
    __slots__ = ["event", "receipt", "transaction"]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    event: Event
    receipt: TransactionReceipt
    transaction: Transaction
    def __init__(
        self,
        transaction: _Optional[_Union[Transaction, _Mapping]] = ...,
        receipt: _Optional[_Union[TransactionReceipt, _Mapping]] = ...,
        event: _Optional[_Union[Event, _Mapping]] = ...,
    ) -> None: ...

class InvokeTransactionV0(_message.Message):
    __slots__ = ["calldata", "contract_address", "entry_point_selector"]
    CALLDATA_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ENTRY_POINT_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    calldata: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    contract_address: _types_pb2.FieldElement
    entry_point_selector: _types_pb2.FieldElement
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        entry_point_selector: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        calldata: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
    ) -> None: ...

class InvokeTransactionV1(_message.Message):
    __slots__ = ["calldata", "sender_address"]
    CALLDATA_FIELD_NUMBER: _ClassVar[int]
    SENDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    calldata: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    sender_address: _types_pb2.FieldElement
    def __init__(
        self,
        sender_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        calldata: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
    ) -> None: ...

class L1HandlerTransaction(_message.Message):
    __slots__ = ["calldata", "contract_address", "entry_point_selector"]
    CALLDATA_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ENTRY_POINT_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    calldata: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    contract_address: _types_pb2.FieldElement
    entry_point_selector: _types_pb2.FieldElement
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        entry_point_selector: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        calldata: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
    ) -> None: ...

class L2ToL1Message(_message.Message):
    __slots__ = ["from_address", "index", "payload", "to_address"]
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    from_address: _types_pb2.FieldElement
    index: int
    payload: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    to_address: _types_pb2.FieldElement
    def __init__(
        self,
        to_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        payload: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        index: _Optional[int] = ...,
        from_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class L2ToL1MessageWithTransaction(_message.Message):
    __slots__ = ["message", "receipt", "transaction"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    message: L2ToL1Message
    receipt: TransactionReceipt
    transaction: Transaction
    def __init__(
        self,
        transaction: _Optional[_Union[Transaction, _Mapping]] = ...,
        receipt: _Optional[_Union[TransactionReceipt, _Mapping]] = ...,
        message: _Optional[_Union[L2ToL1Message, _Mapping]] = ...,
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

class ReplacedClass(_message.Message):
    __slots__ = ["class_hash", "contract_address"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    contract_address: _types_pb2.FieldElement
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class StateDiff(_message.Message):
    __slots__ = [
        "declared_classes",
        "declared_contracts",
        "deployed_contracts",
        "nonces",
        "replaced_classes",
        "storage_diffs",
    ]
    DECLARED_CLASSES_FIELD_NUMBER: _ClassVar[int]
    DECLARED_CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYED_CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    NONCES_FIELD_NUMBER: _ClassVar[int]
    REPLACED_CLASSES_FIELD_NUMBER: _ClassVar[int]
    STORAGE_DIFFS_FIELD_NUMBER: _ClassVar[int]
    declared_classes: _containers.RepeatedCompositeFieldContainer[DeclaredClass]
    declared_contracts: _containers.RepeatedCompositeFieldContainer[DeclaredContract]
    deployed_contracts: _containers.RepeatedCompositeFieldContainer[DeployedContract]
    nonces: _containers.RepeatedCompositeFieldContainer[NonceUpdate]
    replaced_classes: _containers.RepeatedCompositeFieldContainer[ReplacedClass]
    storage_diffs: _containers.RepeatedCompositeFieldContainer[StorageDiff]
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

class Transaction(_message.Message):
    __slots__ = [
        "declare",
        "deploy",
        "deploy_account",
        "invoke_v0",
        "invoke_v1",
        "l1_handler",
        "meta",
    ]
    DECLARE_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_FIELD_NUMBER: _ClassVar[int]
    INVOKE_V0_FIELD_NUMBER: _ClassVar[int]
    INVOKE_V1_FIELD_NUMBER: _ClassVar[int]
    L1_HANDLER_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    declare: DeclareTransaction
    deploy: DeployTransaction
    deploy_account: DeployAccountTransaction
    invoke_v0: InvokeTransactionV0
    invoke_v1: InvokeTransactionV1
    l1_handler: L1HandlerTransaction
    meta: TransactionMeta
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
    __slots__ = ["hash", "max_fee", "nonce", "signature", "version"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    MAX_FEE_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    hash: _types_pb2.FieldElement
    max_fee: _types_pb2.FieldElement
    nonce: _types_pb2.FieldElement
    signature: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
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

class TransactionReceipt(_message.Message):
    __slots__ = [
        "actual_fee",
        "contract_address",
        "events",
        "l2_to_l1_messages",
        "transaction_hash",
        "transaction_index",
    ]
    ACTUAL_FEE_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    L2_TO_L1_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_HASH_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_INDEX_FIELD_NUMBER: _ClassVar[int]
    actual_fee: _types_pb2.FieldElement
    contract_address: _types_pb2.FieldElement
    events: _containers.RepeatedCompositeFieldContainer[Event]
    l2_to_l1_messages: _containers.RepeatedCompositeFieldContainer[L2ToL1Message]
    transaction_hash: _types_pb2.FieldElement
    transaction_index: int
    def __init__(
        self,
        transaction_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        transaction_index: _Optional[int] = ...,
        actual_fee: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        l2_to_l1_messages: _Optional[_Iterable[_Union[L2ToL1Message, _Mapping]]] = ...,
        events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class TransactionWithReceipt(_message.Message):
    __slots__ = ["receipt", "transaction"]
    RECEIPT_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    receipt: TransactionReceipt
    transaction: Transaction
    def __init__(
        self,
        transaction: _Optional[_Union[Transaction, _Mapping]] = ...,
        receipt: _Optional[_Union[TransactionReceipt, _Mapping]] = ...,
    ) -> None: ...

class BlockStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
