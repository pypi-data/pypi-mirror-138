import anyio

DEFAULT_MAX_BITS: int = 64


async def write_unsigned_varint(
    stream: anyio.abc.SocketStream, integer: int, max_bits: int = DEFAULT_MAX_BITS
) -> None:
    max_int: int = 1 << max_bits
    if integer < 0:
        raise ValueError(f"negative integer: {integer}")
    if integer >= max_int:
        raise ValueError(f"integer too large: {integer}")
    while True:
        value: int = integer & 0x7F
        integer >>= 7
        if integer != 0:
            value |= 0x80
        byte = value.to_bytes(1, "big")
        await stream.send_all(byte)
        if integer == 0:
            break


async def read_unsigned_varint(
    stream: anyio.abc.SocketStream, max_bits: int = DEFAULT_MAX_BITS
) -> int:
    max_int: int = 1 << max_bits
    iteration: int = 0
    result: int = 0
    has_next: bool = True
    while has_next:
        data = await stream.receive_exactly(1)
        c = data[0]
        value = c & 0x7F
        result |= value << (iteration * 7)
        has_next = (c & 0x80) != 0
        iteration += 1
        if result >= max_int:
            raise ValueError(f"varint overflowed: {result}")
    return result
