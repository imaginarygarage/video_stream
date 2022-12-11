import cv2
import socket

import packetize


DEFAULT_HOST = ''
DEFAULT_PORT = 8089

stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream_socket.bind((DEFAULT_HOST, DEFAULT_PORT))
stream_socket.listen()
stream, address = stream_socket.accept()
print(f'Connected to stream from {address}')

while True:
    rx_data = stream.recv(packetize.HEADER_SIZE)
    payload_size = packetize.decode_header(rx_data)
    rx_data += stream.recv(payload_size)
    image = packetize.decode_packet(rx_data)
    
    cv2.imshow('rx image', image)
    cv2.waitKey(1)
