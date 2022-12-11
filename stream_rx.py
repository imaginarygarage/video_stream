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

image_fragments = {}
image_id = -1
image_shape = None
fragment_count = 0
while True:
    serialized_packet, address = stream_socket.recvfrom(65000)
    packet = packetize.decode_packet(serialized_packet)

    if image_id != packet['image_id']:
        if len(image_fragments) != fragment_count:
            print(f"Dropped image {image_id}")
        image_id = packet['image_id']
        image_shape = packet['image_shape']
        fragment_count = packet['fragment_count']
        image_fragments = {}
    fragment_index = packet['fragment_index']
    
    image_fragments[fragment_index] = packet.copy()

    if len(image_fragments) == fragment_count:
        image = np.zeros(image_shape, np.uint8)
        for fragment_index in image_fragments:
            packet = image_fragments[fragment_index]
            row_start = packet['fragment_row_start']
            row_end = packet['fragment_row_end']
            image[row_start:row_end, :, :] = packet['image_fragment']
        cv2.imshow('rx image', image)
        cv2.waitKey(1)
        print(f"Image {image_id} displayed")
