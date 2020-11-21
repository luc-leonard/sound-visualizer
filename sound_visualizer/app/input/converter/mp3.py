import logging
import uuid

import ffmpeg

logger = logging.getLogger(__name__)


class Mp3Converter:
    def convert(self, filename: str) -> str:
        the_filename = f'/tmp/{str(uuid.uuid4())}.wav'
        logger.info(f'converting {filename} to wav')
        ffmpeg.input(filename).output(the_filename, loglevel='info').run()
        logger.info(f'{filename} converted to wav at {the_filename}')
        return the_filename
