from .audio_segment import WavSubChunk
import struct

class AudioStream:
    # Read a finite number of bytes
    def read(self, size):
        tmp = self._fd.read(size)
        self._pos += size
        return tmp

    def extract_wav_headers(self):
        self.fastforward(12)  # The size of the RIFF chunk descriptor
        subchunks = []
        while len(subchunks) < 10:
            data = self.read(8)
            subchunk_id = data[0:4]
            subchunk_size = struct.unpack_from('<I', data[4:8])[0]
            subchunks.append(WavSubChunk(subchunk_id, self._pos-8, subchunk_size))
            if subchunk_id == b'data':
                # 'data' is the last subchunk
                break
            self.fastforward(self._pos + subchunk_size)
        return subchunks

    # Provide forward seek-like behavior to help with loading headers
    def fastforward(self, newpos):
        if self._pos > newpos:
            raise ValueError("Cannot fast-forward to {}; Already at {}".format(newpos, self._pos))
        self.read(newpos - self._pos)

    def __init__(self, stream):
        self._fd = stream
        self._pos = 0
        headers = self.extract_wav_headers()
        print(headers)
