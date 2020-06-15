from .audio_segment import extract_wav_headers

class AudioStream:
    def read(self, size = None):
        return self._fd.read(size)

    # Read from file descriptor until 'data' header subchunk is found
    def read_headers(self):
        self.read(12)  # The size of the RIFF chunk descriptor
        subchunks = 0
        buffer = bytearray()
        while subchunks < 10:
            data = self.read(8)
            subchunk_id = data[0:4]
            print("Subchunk: " + subchunk_id.decode())
            buffer.extend(data)
            if subchunk_id == b'data':
                # 'data' is the last subchunk
                print("Found data, exiting")
                break

        return buffer

    # Provide forward seek-like behavior to help with loading headers
    def fastforward(self, newpos):
        if self._pos > newpos:
            raise ValueError("Cannot fast-forward to {}; Already at {}".format(newpos, self._pos))

    def __init__(self, stream):
        self._fd = stream
        self._pos = 0
        headers = extract_wav_headers(self.read_headers())
        print(headers)
