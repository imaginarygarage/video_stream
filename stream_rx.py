import cv2
import numpy as np
import socket
import struct

import packetize


DEFAULT_HOST = ''
DEFAULT_PORT = 8089

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the datagram socket
stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
stream_socket.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
stream_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

image_decoder = packetize.ImageDecoder()
while True:
    serialized_packet, address = stream_socket.recvfrom(65000)
    image = image_decoder.push_fragment(serialized_packet)
    if image is not None:
        cv2.imshow('rx image', image)
        cv2.waitKey(1)
        print(f"Image {image_decoder.image_id} displayed")
