import logging
import uuid

import ffmpeg

from sound_visualizer.app.input.converter.converter import Converter

logger = logging.getLogger(__name__)


class Mp3Converter(Converter):
    def convert(self) -> str:
        the_filename = f'/tmp/{str(uuid.uuid4())}.wav'
        logger.info(f'converting {self.filename} to wav')
        input = ffmpeg.input(self.filename)
        if self.length != -1:
            input = input.filter('atrim', start=self.start, duration=self.length)
        elif self.start != 0:
            input = input.filter('atrim', start=self.start)
        logger.debug(input.output(the_filename, loglevel='info'))
        input.output(the_filename, loglevel='info').run()
        logger.info(f'{self.filename} converted to wav at {the_filename}')
        return the_filename
