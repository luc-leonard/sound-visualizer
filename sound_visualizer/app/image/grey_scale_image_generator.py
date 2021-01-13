import logging
from typing import Generator

import numpy as np
import PIL
from PIL import Image, ImageEnhance, ImageFont, ImageOps
from pydantic import BaseModel

from sound_visualizer.app.sound import SpectralAnalysis
from sound_visualizer.utils import convert_size

logger = logging.getLogger(__name__)


class GreyScaleImageGenerator(BaseModel):
    border_width: int = 30
    border_color: str = 'red'
    frequencies_marks: bool = True
    time_marks: bool = True
    log_scale: bool = False

    def create_image(
        self, spectral_analysis: SpectralAnalysis
    ) -> Generator[PIL.Image.Image, None, None]:
        current_top = 0
        for frame in spectral_analysis.fft_data:
            image_data = np.floor((frame / (frame.max() / 255))).astype('uint8')
            logger.info(
                f'converted fft data to image. shape: {frame.shape} -> {image_data.shape}'
                f'size: {convert_size(image_data.nbytes)}'
            )

            image = ImageOps.expand(
                Image.fromarray(image_data).convert('L'),
                border=(self.border_width, 0, self.border_width, 0),
                fill=self.border_color,
            )
            image = ImageEnhance.Contrast(image).enhance(5.0)

            ImageFont.load_default()
            # draw = ImageDraw.Draw(image)
            # begin_time_for_image = int(np.floor(spectral_analysis.time_domain[current_top]))
            # if current_top + image.height < len(spectral_analysis.time_domain):
            #     end_time_for_image = int(
            #         np.ceil(spectral_analysis.time_domain[current_top + image.height])
            #     )
            # else:
            #     end_time_for_image = int(np.ceil(spectral_analysis.time_domain[-1]))
            # logger.info(f'begin_time = {begin_time_for_image}, end_time = {end_time_for_image}')
            # for i in range(begin_time_for_image, end_time_for_image, 1):
            #     second_idx = spectral_analysis.time_domain.searchsorted(i) - current_top
            #     draw.line([(0, second_idx), (15, second_idx)], fill='red', width=1)
            #     if i % 5 == 0:
            #         draw.text(xy=(0, second_idx + 16), text=f'{i}', fill='red')
            #
            # for j in [10, 100, 1000, 10000]:
            #     frequency_idx = spectral_analysis.frequency_domain.searchsorted(j)
            #     draw.line(
            #         [(frequency_idx + 15, 0), (frequency_idx + 15, image.size[1])],
            #         fill='red',
            #         width=1,
            #     )
            current_top += image.height
            yield image.rotate(90, expand=True)
