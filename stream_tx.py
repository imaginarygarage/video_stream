import cv2
import socket

import packetize


DEFAULT_CAMERA_INDEX = 0
DEFAULT_PORT = 8089

stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream_socket.connect(('192.168.0.148', DEFAULT_PORT))

camera = cv2.VideoCapture(DEFAULT_CAMERA_INDEX)

while True:
    read_success, image = camera.read()
    if read_success:
        packet = packetize.encode_packet(image)
        stream_socket.sendall(packet)
