import logging
import uuid

import ffmpeg

from sound_visualizer.app.input.converter.converter import Converter

logger = logging.getLogger(__name__)


class Mp3Converter(Converter):
    def convert(self, filename: str, start: int = 0, length: int = -1) -> str:
        the_filename = f'/tmp/{str(uuid.uuid4())}.wav'
        logger.info(f'converting {filename} to wav')
        input = ffmpeg.input(filename)
        if length != -1:
            input = input.filter('atrim', start=start, duration=length)
        elif start != 0:
            input = input.filter('atrim', start=start)
        logger.debug(input.output(the_filename, loglevel='info'))
        input.output(the_filename, loglevel='info').run()
        logger.info(f'{filename} converted to wav at {the_filename}')
        return the_filename
