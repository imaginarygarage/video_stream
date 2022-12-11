import cv2
import numpy as np
import socket

import packetize


DEFAULT_CAMERA_INDEX = 0
DEFAULT_IP = '224.3.29.71'
DEFAULT_PORT = 10000
DEFAULT_MAX_PACKET_SIZE = 60000

multicast_group = (DEFAULT_IP, DEFAULT_PORT)

# Create the datagram socket
stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = b'\x01' # allow one hop (stays withing LAN)
stream_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

camera = cv2.VideoCapture(DEFAULT_CAMERA_INDEX)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
image_id = 0

while True:
    read_success, image = camera.read()
    if read_success:
        # image = np.zeros((11,11,3), dtype=np.uint8)
        # image[5,5,:] = 255
        width = image.shape[1]
        height = image.shape[0]
        fragment_height = min(DEFAULT_MAX_PACKET_SIZE // (3 * width), height)
        fragments = height // fragment_height
        fragments += 1 if fragments * fragment_height < height else 0
        for i in range(fragments):
            row_start = i * fragment_height
            row_end = min(row_start + fragment_height, height)
            image_fragment = image[row_start:row_end, :, :]
            packet = packetize.encode_packet(image_fragment, image_id, image.shape, row_start, row_end, i, fragments)
            stream_socket.sendto(packet, multicast_group)
        image_id += 1
