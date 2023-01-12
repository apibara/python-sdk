import apibara.starknet.felt as felt


def test_encoding():
    hash = "0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3"
    encoded = felt.from_hex(hash)
    back = felt.to_hex(encoded)
    assert hash == back


def test_encoding_as_big_endian():
    prime = 2**251 + 17 * 2**192
    encoded = felt.from_int(prime)
    assert encoded.hi_hi == 0
    assert encoded.hi_lo == 0
    assert encoded.lo_hi == 0
    assert encoded.lo_lo == 576460752303423505
