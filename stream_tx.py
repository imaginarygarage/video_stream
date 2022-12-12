import cv2
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
        encoded_image = packetize.EncodeImage(image, image_id)
        image_id += 1
        for fragment in encoded_image.fragments:
            stream_socket.sendto(fragment, multicast_group)
