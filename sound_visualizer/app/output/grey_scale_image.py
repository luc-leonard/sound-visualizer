import numpy as np
from PIL import Image, ImageOps
from pydantic import BaseModel


class GreyScaleImageGenerator(BaseModel):
    border_width: int
    border_color: str

    def create_image(self, fft_data: np.ndarray) -> Image:
        image_data = np.floor((fft_data / (fft_data.max() / 255))).astype('uint8')
        return ImageOps.expand(
            Image.fromarray(image_data), border=self.border_width, fill=self.border_color
        )
