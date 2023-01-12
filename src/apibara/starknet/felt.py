from apibara.starknet.proto.types_pb2 import FieldElement


def to_int(felt: FieldElement) -> int:
    """
    Convert the wire-encoded field element to an int.

    Arguments
    ---------
    felt : FieldElement
        the protobuf field element object.
    """
    return (felt.lo_lo << 192) + (felt.lo_hi << 128) + (felt.hi_lo << 64) + felt.hi_hi


def to_hex(felt: FieldElement) -> str:
    """
    Convert the wire-encoded field element to hex.

    Arguments
    ---------
    felt : FieldElement
        the protobuf field element object.
    """
    return "0x" + _normalize_hex(hex(to_int(felt)))


def from_int(num: int) -> FieldElement:
    """
    Create a new wire-encoded field element from an int.

    Arguments
    ---------
    num : int
        the number
    """
    return from_hex(hex(num))


def from_hex(h: str) -> FieldElement:
    """
    Create a new wire-encoded field element from a hex string.

    Arguments
    ---------
    h : str
        the hex string. can start with 0.
    """
    h = _normalize_hex(h)
    s = len(h)
    lo_lo = int(h[0:16], 16)
    lo_hi = int(h[16:32], 16)
    hi_lo = int(h[32:48], 16)
    hi_hi = int(h[48:64], 16)
    return FieldElement(
        lo_lo=lo_lo,
        lo_hi=lo_hi,
        hi_lo=hi_lo,
        hi_hi=hi_hi,
    )


def _normalize_hex(h: str) -> str:
    return h.replace("0x", "").rjust(64, "0")
