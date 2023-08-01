from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class DataFinality(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DATA_STATUS_UNKNOWN: _ClassVar[DataFinality]
    DATA_STATUS_PENDING: _ClassVar[DataFinality]
    DATA_STATUS_ACCEPTED: _ClassVar[DataFinality]
    DATA_STATUS_FINALIZED: _ClassVar[DataFinality]

DATA_STATUS_UNKNOWN: DataFinality
DATA_STATUS_PENDING: DataFinality
DATA_STATUS_ACCEPTED: DataFinality
DATA_STATUS_FINALIZED: DataFinality

class StreamDataRequest(_message.Message):
    __slots__ = ["stream_id", "batch_size", "starting_cursor", "finality", "filter"]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    STARTING_CURSOR_FIELD_NUMBER: _ClassVar[int]
    FINALITY_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    stream_id: int
    batch_size: int
    starting_cursor: Cursor
    finality: DataFinality
    filter: bytes
    def __init__(
        self,
        stream_id: _Optional[int] = ...,
        batch_size: _Optional[int] = ...,
        starting_cursor: _Optional[_Union[Cursor, _Mapping]] = ...,
        finality: _Optional[_Union[DataFinality, str]] = ...,
        filter: _Optional[bytes] = ...,
    ) -> None: ...

class StreamDataResponse(_message.Message):
    __slots__ = ["stream_id", "invalidate", "data", "heartbeat"]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    INVALIDATE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    stream_id: int
    invalidate: Invalidate
    data: Data
    heartbeat: Heartbeat
    def __init__(
        self,
        stream_id: _Optional[int] = ...,
        invalidate: _Optional[_Union[Invalidate, _Mapping]] = ...,
        data: _Optional[_Union[Data, _Mapping]] = ...,
        heartbeat: _Optional[_Union[Heartbeat, _Mapping]] = ...,
    ) -> None: ...

class Cursor(_message.Message):
    __slots__ = ["order_key", "unique_key"]
    ORDER_KEY_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_KEY_FIELD_NUMBER: _ClassVar[int]
    order_key: int
    unique_key: bytes
    def __init__(
        self, order_key: _Optional[int] = ..., unique_key: _Optional[bytes] = ...
    ) -> None: ...

class Invalidate(_message.Message):
    __slots__ = ["cursor"]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    cursor: Cursor
    def __init__(self, cursor: _Optional[_Union[Cursor, _Mapping]] = ...) -> None: ...

class Data(_message.Message):
    __slots__ = ["end_cursor", "finality", "data", "cursor"]
    END_CURSOR_FIELD_NUMBER: _ClassVar[int]
    FINALITY_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    end_cursor: Cursor
    finality: DataFinality
    data: _containers.RepeatedScalarFieldContainer[bytes]
    cursor: Cursor
    def __init__(
        self,
        end_cursor: _Optional[_Union[Cursor, _Mapping]] = ...,
        finality: _Optional[_Union[DataFinality, str]] = ...,
        data: _Optional[_Iterable[bytes]] = ...,
        cursor: _Optional[_Union[Cursor, _Mapping]] = ...,
    ) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
