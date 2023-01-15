from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from apibara.protocol.proto.stream_pb2 import Cursor, DataFinality

Data = TypeVar("Data")
Filter = TypeVar("Filter")


@dataclass
class IndexerConfiguration(Generic[Filter]):
    filter: Filter
    starting_cursor: Optional[Cursor] = None
    finality: Optional[DataFinality.ValueType] = None
