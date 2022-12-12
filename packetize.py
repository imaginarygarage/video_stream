import numpy as np
import pickle


DEFAULT_MAX_PACKET_SIZE = 60000

class EncodeImage:
    def __init__(self, image, id):
        self.image = image
        self.image_id = id
        self.image_shape = image.shape
        self.image_height = image.shape[0]
        self.image_width = image.shape[1]
        self.fragment_height = min(DEFAULT_MAX_PACKET_SIZE // (3 * self.image_width), self.image_height)
        self.fragment_count = self.image_height // self.fragment_height
        self.fragment_count += 1 if self.fragment_count * self.fragment_height < self.image_height else 0
        self.fragments = []
        for i in range(self.fragment_count):
            self.fragments.append(self.encode_image_fragment(i))

    def encode_image_fragment(self, fragment_index) -> bytes:
        row_start = fragment_index * self.fragment_height
        row_end = min(row_start + self.fragment_height, self.image_height)
        packet = {}
        packet['image_id'] = self.image_id
        packet['image_shape'] = self.image_shape
        packet['image_fragment'] = self.image[row_start:row_end, :, :]
        packet['fragment_index'] = fragment_index
        packet['fragment_count'] = self.fragment_count
        packet['fragment_row_start'] = row_start
        packet['fragment_row_end'] = row_end
        serialized_packet = pickle.dumps(packet)
        return serialized_packet

class ImageDecoder:
    def __init__(self):
        self.image_fragments = {}
        self.image_id = -1
        self.image_shape = None
        self.image = None
        self.fragment_count = 0
    
    def push_fragment(self, fragment):
        fragment_data = self.decode_fragment(fragment)
        if self.image_id != fragment_data['image_id']:
            if len(self.image_fragments) != self.fragment_count:
                print(f"Dropped image {self.image_id}")
            self.image_id = fragment_data['image_id']
            self.image_shape = fragment_data['image_shape']
            self.fragment_count = fragment_data['fragment_count']
            self.image_fragments = {}
            self.image = None
        fragment_index = fragment_data['fragment_index']
        self.image_fragments[fragment_index] = fragment_data.copy()
        if len(self.image_fragments) == self.fragment_count:
            self.image = np.zeros(self.image_shape, np.uint8)
            for fragment_index in self.image_fragments:
                fragment_data = self.image_fragments[fragment_index]
                row_start = fragment_data['fragment_row_start']
                row_end = fragment_data['fragment_row_end']
                self.image[row_start:row_end, :, :] = fragment_data['image_fragment']
        return self.image

    def decode_fragment(self, serialized_fragment: bytes):
        fragment = pickle.loads(serialized_fragment)
        return fragment
