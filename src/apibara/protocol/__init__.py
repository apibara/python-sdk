from dataclasses import dataclass
from typing import ClassVar

from .client import (BearerTokenAuth, StreamClient, StreamIter, StreamService,
                     credentials_with_auth_token)
from .proto.stream_pb2 import (Cursor, DataFinality, StreamDataRequest,
                               StreamDataResponse)


@dataclass
class StarkNetStreamAddress:
    Mainnet: ClassVar[str] = "mainnet.starknet.a5a.ch"
    Goerli: ClassVar[str] = "goerli.starknet.a5a.ch"
    Goerli2: ClassVar[str] = "goerli-2.starknet.a5a.ch"


@dataclass
class StreamAddress:
    """Defines well-known addresses for the Apibara Stream service."""

    StarkNet: ClassVar[StarkNetStreamAddress] = StarkNetStreamAddress
