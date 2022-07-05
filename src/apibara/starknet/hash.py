from eth_hash.auto import keccak

_MASK_250 = 2**250 - 1


def get_selector_from_name(func_name: str) -> int:
    """Get the selector for the given function name."""
    # This function comes from cairo-lang, but we want to
    # avoid that dependency to simplify installation.
    return _starknet_keccak(data=func_name.encode("ascii"))


def _starknet_keccak(data: bytes) -> int:
    return int.from_bytes(keccak(data), "big") & _MASK_250
