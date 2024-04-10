import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class Filter(_message.Message):
    __slots__ = ["header", "transactions", "state_update", "events", "messages"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    STATE_UPDATE_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    header: HeaderFilter
    transactions: _containers.RepeatedCompositeFieldContainer[TransactionFilter]
    state_update: StateUpdateFilter
    events: _containers.RepeatedCompositeFieldContainer[EventFilter]
    messages: _containers.RepeatedCompositeFieldContainer[L2ToL1MessageFilter]
    def __init__(
        self,
        header: _Optional[_Union[HeaderFilter, _Mapping]] = ...,
        transactions: _Optional[_Iterable[_Union[TransactionFilter, _Mapping]]] = ...,
        state_update: _Optional[_Union[StateUpdateFilter, _Mapping]] = ...,
        events: _Optional[_Iterable[_Union[EventFilter, _Mapping]]] = ...,
        messages: _Optional[_Iterable[_Union[L2ToL1MessageFilter, _Mapping]]] = ...,
    ) -> None: ...

class HeaderFilter(_message.Message):
    __slots__ = ["weak"]
    WEAK_FIELD_NUMBER: _ClassVar[int]
    weak: bool
    def __init__(self, weak: bool = ...) -> None: ...

class TransactionFilter(_message.Message):
    __slots__ = [
        "invoke_v0",
        "invoke_v1",
        "deploy",
        "declare",
        "l1_handler",
        "deploy_account",
        "include_reverted",
    ]
    INVOKE_V0_FIELD_NUMBER: _ClassVar[int]
    INVOKE_V1_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_FIELD_NUMBER: _ClassVar[int]
    DECLARE_FIELD_NUMBER: _ClassVar[int]
    L1_HANDLER_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_REVERTED_FIELD_NUMBER: _ClassVar[int]
    invoke_v0: InvokeTransactionV0Filter
    invoke_v1: InvokeTransactionV1Filter
    deploy: DeployTransactionFilter
    declare: DeclareTransactionFilter
    l1_handler: L1HandlerTransactionFilter
    deploy_account: DeployAccountTransactionFilter
    include_reverted: bool
    def __init__(
        self,
        invoke_v0: _Optional[_Union[InvokeTransactionV0Filter, _Mapping]] = ...,
        invoke_v1: _Optional[_Union[InvokeTransactionV1Filter, _Mapping]] = ...,
        deploy: _Optional[_Union[DeployTransactionFilter, _Mapping]] = ...,
        declare: _Optional[_Union[DeclareTransactionFilter, _Mapping]] = ...,
        l1_handler: _Optional[_Union[L1HandlerTransactionFilter, _Mapping]] = ...,
        deploy_account: _Optional[
            _Union[DeployAccountTransactionFilter, _Mapping]
        ] = ...,
        include_reverted: bool = ...,
    ) -> None: ...

class InvokeTransactionV0Filter(_message.Message):
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

class InvokeTransactionV1Filter(_message.Message):
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

class DeployTransactionFilter(_message.Message):
    __slots__ = ["contract_address_salt", "class_hash", "constructor_calldata"]
    CONTRACT_ADDRESS_SALT_FIELD_NUMBER: _ClassVar[int]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    CONSTRUCTOR_CALLDATA_FIELD_NUMBER: _ClassVar[int]
    contract_address_salt: _types_pb2.FieldElement
    class_hash: _types_pb2.FieldElement
    constructor_calldata: _containers.RepeatedCompositeFieldContainer[
        _types_pb2.FieldElement
    ]
    def __init__(
        self,
        contract_address_salt: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        constructor_calldata: _Optional[
            _Iterable[_Union[_types_pb2.FieldElement, _Mapping]]
        ] = ...,
    ) -> None: ...

class DeclareTransactionFilter(_message.Message):
    __slots__ = ["class_hash", "sender_address"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    SENDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    sender_address: _types_pb2.FieldElement
    def __init__(
        self,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        sender_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class L1HandlerTransactionFilter(_message.Message):
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

class DeployAccountTransactionFilter(_message.Message):
    __slots__ = ["contract_address_salt", "class_hash", "constructor_calldata"]
    CONTRACT_ADDRESS_SALT_FIELD_NUMBER: _ClassVar[int]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    CONSTRUCTOR_CALLDATA_FIELD_NUMBER: _ClassVar[int]
    contract_address_salt: _types_pb2.FieldElement
    class_hash: _types_pb2.FieldElement
    constructor_calldata: _containers.RepeatedCompositeFieldContainer[
        _types_pb2.FieldElement
    ]
    def __init__(
        self,
        contract_address_salt: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        constructor_calldata: _Optional[
            _Iterable[_Union[_types_pb2.FieldElement, _Mapping]]
        ] = ...,
    ) -> None: ...

class L2ToL1MessageFilter(_message.Message):
    __slots__ = ["to_address", "payload", "include_reverted"]
    TO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_REVERTED_FIELD_NUMBER: _ClassVar[int]
    to_address: _types_pb2.FieldElement
    payload: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    include_reverted: bool
    def __init__(
        self,
        to_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        payload: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        include_reverted: bool = ...,
    ) -> None: ...

class EventFilter(_message.Message):
    __slots__ = [
        "from_address",
        "keys",
        "data",
        "include_reverted",
        "include_transaction",
        "include_receipt",
    ]
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_REVERTED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_RECEIPT_FIELD_NUMBER: _ClassVar[int]
    from_address: _types_pb2.FieldElement
    keys: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    data: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    include_reverted: bool
    include_transaction: bool
    include_receipt: bool
    def __init__(
        self,
        from_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        keys: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        data: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        include_reverted: bool = ...,
        include_transaction: bool = ...,
        include_receipt: bool = ...,
    ) -> None: ...

class StateUpdateFilter(_message.Message):
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
    storage_diffs: _containers.RepeatedCompositeFieldContainer[StorageDiffFilter]
    declared_contracts: _containers.RepeatedCompositeFieldContainer[
        DeclaredContractFilter
    ]
    deployed_contracts: _containers.RepeatedCompositeFieldContainer[
        DeployedContractFilter
    ]
    nonces: _containers.RepeatedCompositeFieldContainer[NonceUpdateFilter]
    declared_classes: _containers.RepeatedCompositeFieldContainer[DeclaredClassFilter]
    replaced_classes: _containers.RepeatedCompositeFieldContainer[ReplacedClassFilter]
    def __init__(
        self,
        storage_diffs: _Optional[_Iterable[_Union[StorageDiffFilter, _Mapping]]] = ...,
        declared_contracts: _Optional[
            _Iterable[_Union[DeclaredContractFilter, _Mapping]]
        ] = ...,
        deployed_contracts: _Optional[
            _Iterable[_Union[DeployedContractFilter, _Mapping]]
        ] = ...,
        nonces: _Optional[_Iterable[_Union[NonceUpdateFilter, _Mapping]]] = ...,
        declared_classes: _Optional[
            _Iterable[_Union[DeclaredClassFilter, _Mapping]]
        ] = ...,
        replaced_classes: _Optional[
            _Iterable[_Union[ReplacedClassFilter, _Mapping]]
        ] = ...,
    ) -> None: ...

class StorageDiffFilter(_message.Message):
    __slots__ = ["contract_address"]
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    contract_address: _types_pb2.FieldElement
    def __init__(
        self,
        contract_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
    ) -> None: ...

class DeclaredContractFilter(_message.Message):
    __slots__ = ["class_hash"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    def __init__(
        self, class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...
    ) -> None: ...

class DeclaredClassFilter(_message.Message):
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

class ReplacedClassFilter(_message.Message):
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

class DeployedContractFilter(_message.Message):
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

class NonceUpdateFilter(_message.Message):
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
