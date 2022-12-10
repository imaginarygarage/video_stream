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

rx_data = b''
while True:
    while len(rx_data) < packetize.HEADER_SIZE:
        rx_data += stream.recv(4096)
    payload_size = packetize.decode_header(rx_data)
    packet_size = packetize.HEADER_SIZE + payload_size

    while len(rx_data) < packet_size:
        rx_data += stream.recv(4096)
    image = packetize.decode_packet(rx_data)
    
    cv2.imshow('rx image', image)
    cv2.waitKey(1)

    rx_data = rx_data[packet_size:]

    if len(rx_data) > 0:
        print(f"leftovers size: {len(rx_data)}")
