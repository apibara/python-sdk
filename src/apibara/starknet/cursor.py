from typing import Optional, Union

import apibara.starknet.felt as felt
from apibara.protocol.proto.stream_pb2 import Cursor
from apibara.starknet.proto.types_pb2 import FieldElement


def starknet_cursor(
    block_number: int, block_hash: Optional[Union[bytes, str, FieldElement]] = None
) -> Cursor:
    """
    Create a new StarkNet cursor for the given block number and block hash.

    Arguments
    ---------
    block_number : int
        block height
    block_hash : bytes | str | FieldElement, optional
        block hash
    """
    if block_hash is not None:
        unique_key = _to_bytes(block_hash)
    else:
        unique_key = b""
    return Cursor(order_key=block_number, unique_key=unique_key)


def _to_bytes(hash: Union[bytes, str, FieldElement]) -> bytes:
    if isinstance(hash, bytes):
        return hash

    if isinstance(hash, FieldElement):
        hash = felt.to_hex(hash)

    if isinstance(hash, str):
        return bytes.fromhex(hash)

    raise ValueError("hash must be bytes, str, or FieldElement")
