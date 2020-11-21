import uuid

import ffmpeg


class Mp3Converter:
    def convert(self, filename: str) -> str:
        filename = str(uuid.uuid4()) + '.wav'
        ffmpeg.input(filename).output(filename)
        return filename
