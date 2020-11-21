import uuid

import ffmpeg


class Mp3Converter:
    def convert(self, filename: str) -> str:
        the_filename = f'/tmp/{str(uuid.uuid4())}.wav'
        ffmpeg.input(filename).output(the_filename, loglevel='info').run()
        return the_filename
