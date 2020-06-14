from .audio_segment import WavSubChunk

import struct

class AudioStream:
    def read(self, size = None):
        return self._fd.read(size)

    def extract_wav_headers(self):
        self.read(12)  # The size of the RIFF chunk descriptor

        # TODO we need to return the actual position (pos)
        pos = 12
        subchunks = []
        while len(subchunks) < 10:
            data = self.read(8)
            subchunk_id = data[0:4]
            subchunk_size = struct.unpack_from('<I', data[4:8])[0]
            subchunks.append(WavSubChunk(subchunk_id, pos, subchunk_size))
            if subchunk_id == b'data':
                # 'data' is the last subchunk
                break
            pos += subchunk_size + 8

        return subchunks


    def __init__(self, stream):
        self._fd = stream
        # Assume the header is exactly 40 bytes
        headers = self.extract_wav_headers()
        print(headers)
