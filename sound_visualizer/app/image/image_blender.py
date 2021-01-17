from functools import reduce
from typing import Dict, Generator

import PIL
from PIL import Image, ImageOps

_COLORS = {
    'bass': '#FF0000',
    'drums': '#00FF00',
    'vocals': '#0000FF',
    'piano': '#FFFFFF',
    'other': '#FF00FF',
}


def image_tint(src, color="#FFFFFF"):
    gray, alpha = src.split()
    result = ImageOps.colorize(gray, white=color, black="white")
    result.putalpha(alpha)
    return result


###
### receives a dict where each key is an instrument, and each value is a generator of spectrogram.
### each generator MUST yield the same number of items.
###
def greyscale_images_blender(
    greyscale_images: Dict[str, Generator[PIL.Image.Image, None, None]]
) -> Generator[PIL.Image.Image, None, None]:

    while True:
        images = []
        try:
            for instrument in greyscale_images.keys():
                image = next(greyscale_images[instrument])
                image.putalpha(image.copy().convert('L'))
                image = image_tint(image, _COLORS[instrument])
                images.append(image)
            merged_image = reduce(
                lambda left, right: Image.alpha_composite(left, right), images[1:], images[0]
            )
            final_image = Image.new('RGB', merged_image.size, "BLACK")
            final_image.paste(merged_image, (0, 0), merged_image)
            yield final_image
        except Exception as ex:
            print(ex)
            return
