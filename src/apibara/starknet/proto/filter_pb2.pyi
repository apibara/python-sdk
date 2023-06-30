from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

import apibara.starknet.proto.types_pb2 as _types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

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

class DeclaredContractFilter(_message.Message):
    __slots__ = ["class_hash"]
    CLASS_HASH_FIELD_NUMBER: _ClassVar[int]
    class_hash: _types_pb2.FieldElement
    def __init__(
        self, class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...
    ) -> None: ...

class DeployAccountTransactionFilter(_message.Message):
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
        contract_address_salt: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        constructor_calldata: _Optional[
            _Iterable[_Union[_types_pb2.FieldElement, _Mapping]]
        ] = ...,
    ) -> None: ...

class DeployTransactionFilter(_message.Message):
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
        contract_address_salt: _Optional[
            _Union[_types_pb2.FieldElement, _Mapping]
        ] = ...,
        class_hash: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        constructor_calldata: _Optional[
            _Iterable[_Union[_types_pb2.FieldElement, _Mapping]]
        ] = ...,
    ) -> None: ...

class DeployedContractFilter(_message.Message):
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

class EventFilter(_message.Message):
    __slots__ = ["data", "from_address", "keys"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    from_address: _types_pb2.FieldElement
    keys: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    def __init__(
        self,
        from_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        keys: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
        data: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
    ) -> None: ...

class Filter(_message.Message):
    __slots__ = ["events", "header", "messages", "state_update", "transactions"]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    STATE_UPDATE_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[EventFilter]
    header: HeaderFilter
    messages: _containers.RepeatedCompositeFieldContainer[L2ToL1MessageFilter]
    state_update: StateUpdateFilter
    transactions: _containers.RepeatedCompositeFieldContainer[TransactionFilter]
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

class InvokeTransactionV0Filter(_message.Message):
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

class InvokeTransactionV1Filter(_message.Message):
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

class L1HandlerTransactionFilter(_message.Message):
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

class L2ToL1MessageFilter(_message.Message):
    __slots__ = ["payload", "to_address"]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    payload: _containers.RepeatedCompositeFieldContainer[_types_pb2.FieldElement]
    to_address: _types_pb2.FieldElement
    def __init__(
        self,
        to_address: _Optional[_Union[_types_pb2.FieldElement, _Mapping]] = ...,
        payload: _Optional[_Iterable[_Union[_types_pb2.FieldElement, _Mapping]]] = ...,
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

class ReplacedClassFilter(_message.Message):
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

class StateUpdateFilter(_message.Message):
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
    declared_classes: _containers.RepeatedCompositeFieldContainer[DeclaredClassFilter]
    declared_contracts: _containers.RepeatedCompositeFieldContainer[
        DeclaredContractFilter
    ]
    deployed_contracts: _containers.RepeatedCompositeFieldContainer[
        DeployedContractFilter
    ]
    nonces: _containers.RepeatedCompositeFieldContainer[NonceUpdateFilter]
    replaced_classes: _containers.RepeatedCompositeFieldContainer[ReplacedClassFilter]
    storage_diffs: _containers.RepeatedCompositeFieldContainer[StorageDiffFilter]
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

class TransactionFilter(_message.Message):
    __slots__ = [
        "declare",
        "deploy",
        "deploy_account",
        "invoke_v0",
        "invoke_v1",
        "l1_handler",
    ]
    DECLARE_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DEPLOY_FIELD_NUMBER: _ClassVar[int]
    INVOKE_V0_FIELD_NUMBER: _ClassVar[int]
    INVOKE_V1_FIELD_NUMBER: _ClassVar[int]
    L1_HANDLER_FIELD_NUMBER: _ClassVar[int]
    declare: DeclareTransactionFilter
    deploy: DeployTransactionFilter
    deploy_account: DeployAccountTransactionFilter
    invoke_v0: InvokeTransactionV0Filter
    invoke_v1: InvokeTransactionV1Filter
    l1_handler: L1HandlerTransactionFilter
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
    ) -> None: ...
