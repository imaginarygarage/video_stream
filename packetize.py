import serialize


def checksum_8bit(bytes: bytes) -> bytes:
    return serialize.serialize_uint8(sum(bytes) & 0xFF)

def encode_header(serialized_size: int, id=0, index=0, total=1) -> bytes:
    header = serialize.serialize_uint32(serialized_size)
    header += serialize.serialize_uint32(id)
    header += serialize.serialize_uint32(index)
    header += serialize.serialize_uint32(total)
    return header + checksum_8bit(header)

HEADER_SIZE = len(encode_header(0))

def decode_header(header: bytes) -> int:
    valid = validate_header(header)
    if valid:
        serialized_size = serialize.deserialize_uint32(header[:4])[0]
        id = serialize.deserialize_uint32(header[4:8])[0]
        fragment_index = serialize.deserialize_uint32(header[8:12])[0]
        fragments_total = serialize.deserialize_uint32(header[12:16])[0]
        return serialized_size, id, fragment_index, fragments_total
    else:
        return None

def validate_header(header: bytes) -> bool:
    correct_length = len(header) >= HEADER_SIZE
    expected_checksum = checksum_8bit(header[:HEADER_SIZE - 1])
    actual_checksum = header[HEADER_SIZE - 1:HEADER_SIZE]
    correct_checksum = expected_checksum == actual_checksum
    return correct_length and correct_checksum

def encode_packet(image, image_id, image_shape, row_start, row_end, index=0, total=1) -> bytes:
    packet = {}
    packet['image_id'] = image_id
    packet['image_shape'] = image_shape
    packet['image_fragment'] = image
    packet['fragment_index'] = index
    packet['fragment_count'] = total
    packet['fragment_row_start'] = row_start
    packet['fragment_row_end'] = row_end
    serialized_packet = serialize.serialize_image(packet)
    return serialized_packet

def decode_packet(serialized_packet: bytes):
    packet = serialize.deserialize_image(serialized_packet)
    return packet

