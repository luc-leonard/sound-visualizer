import logging

from PIL import Image
from pydantic import BaseModel

from sound_visualizer.app.sound import SpectralAnalysis

logger = logging.getLogger(__name__)


class GreyScaleImageGenerator(BaseModel):
    border_width: int
    border_color: str
    frequencies_marks: bool
    time_marks: bool
    log_scale: bool = False

    def create_image(self, spectral_analysis: SpectralAnalysis) -> Image:
        ...
        # pixel_per_second = spectral_analysis.time_domain.searchsorted(1)
        # images = []
        # image_data = np.floor((fft_data / (fft_data.max() / 255))).astype('uint8')
        # logger.info(
        #     f'converted fft data to image. shape: {fft_data.shape} -> {image_data.shape}'
        #     f'size: {convert_size(image_data.nbytes)}'
        # )
        #
        # return ImageOps.expand(
        #     Image.fromarray(image_data).convert('RGB'),
        #     border=self.border_width,
        #     fill=self.border_color,
        # )
