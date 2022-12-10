import pickle
import struct


PACK_TYPE_UINT8 = "B"
PACK_TYPE_UINT16 = "H"
PACK_TYPE_UINT32 = "L"

def deserialize_uint8(serialized_value: bytes) -> int:
    return struct.unpack(PACK_TYPE_UINT8, serialized_value)

def deserialize_uint16(serialized_value: bytes) -> int:
    return struct.unpack(PACK_TYPE_UINT16, serialized_value)

def deserialize_uint32(serialized_value: bytes) -> int:
    return struct.unpack(PACK_TYPE_UINT32, serialized_value)

def deserialize_image(serialized_image: bytes):
    return pickle.loads(serialized_image)

def serialize_uint8(value: int) -> bytes:
    return struct.pack(PACK_TYPE_UINT8, value)

def serialize_uint16(value: int) -> bytes:
    return struct.pack(PACK_TYPE_UINT16, value)

def serialize_uint32(value: int) -> bytes:
    return struct.pack(PACK_TYPE_UINT32, value)

def serialize_image(image) -> bytes:
    return pickle.dumps(image)
