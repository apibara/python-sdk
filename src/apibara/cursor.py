from apibara.protocol.proto.stream_pb2 import Cursor


def to_json(cursor: Cursor) -> dict:
    """Converts cursor to a json object."""
    return {"order_key": cursor.order_key, "unique_key": cursor.unique_key.hex()}


def from_json(cursor: dict) -> Cursor:
    """Returns a `Cursor` from its json representation."""
    if "unique_key" in cursor:
        unique_key = bytes.fromhex(cursor["unique_key"])
    else:
        unique_key = b""

    return Cursor(order_key=cursor["order_key"], unique_key=unique_key)
