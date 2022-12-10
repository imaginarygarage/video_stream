import serialize


def checksum_8bit(bytes: bytes) -> bytes:
    return serialize.serialize_uint8(sum(bytes) & 0xFF)

def encode_header(serialized_size: int) -> bytes:
    header = serialize.serialize_uint32(serialized_size)
    return header + checksum_8bit(header)

HEADER_SIZE = len(encode_header(0))

def decode_header(header: bytes) -> int:
    valid = validate_header(header)
    serialized_size = serialize.deserialize_uint32(header[:4])[0] if valid else None
    return serialized_size

def validate_header(header: bytes) -> bool:
    correct_length = len(header) >= HEADER_SIZE
    expected_checksum = checksum_8bit(header[:HEADER_SIZE - 1])
    actual_checksum = header[HEADER_SIZE - 1:HEADER_SIZE]
    correct_checksum = expected_checksum == actual_checksum
    return correct_length and correct_checksum

def encode_packet(image) -> bytes:
    serialized_image = serialize.serialize_image(image)
    serialized_image_size = len(serialized_image)
    header = encode_header(serialized_image_size)
    return header + serialized_image

def decode_packet(packet: bytes) -> bytes:
    header = packet[:HEADER_SIZE]
    serialized_image_size = decode_header(header)
    serialized_image = packet[HEADER_SIZE:HEADER_SIZE + serialized_image_size]
    return serialize.deserialize_image(serialized_image)
