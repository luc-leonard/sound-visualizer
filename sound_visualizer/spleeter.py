import logging

from PIL import Image, ImageOps

from sound_visualizer.app.image.grey_scale_image_generator import GreyScaleImageGenerator
from sound_visualizer.app.sound import SoundReader, SpectralAnalyzer
from sound_visualizer.utils import StopWatch


def merge_images(img1: Image.Image, img2: Image.Image) -> Image.Image:
    return Image.alpha_composite(img1, img2)


def to_transparent_bg(image: Image.Image) -> Image.Image:
    image.putalpha(image.copy().convert('L'))
    return image


def image_tint(src, color="#FFFFFF"):
    gray, alpha = src.split()
    result = ImageOps.colorize(gray, white=color, black="white")
    result.putalpha(alpha)
    return result


logging.getLogger().setLevel('DEBUG')

analyser = SpectralAnalyzer(overlap_factor=0.90, frame_size=2 ** 12)
image_generator = GreyScaleImageGenerator(border_width=0)

BASE_FOLDER = '/home/lleonard/dev/perso/sound-visualizer/spleets/pink_floyd_numb/pink_floyd_numb/'
data_vocal = analyser.get_spectrogram_data(SoundReader(filename=BASE_FOLDER + '/vocals.wav'))
data_drums = analyser.get_spectrogram_data(SoundReader(filename=BASE_FOLDER + '/drums.wav'))
data_bass = analyser.get_spectrogram_data(SoundReader(filename=BASE_FOLDER + '/bass.wav'))
data_piano = analyser.get_spectrogram_data(SoundReader(filename=BASE_FOLDER + '/piano.wav'))
data_other = analyser.get_spectrogram_data(SoundReader(filename=BASE_FOLDER + '/other.wav'))


image_vocal = image_generator.create_image(data_vocal)
image_drums = image_generator.create_image(data_drums)
image_bass = image_generator.create_image(data_bass)
image_piano = image_generator.create_image(data_piano)
image_other = image_generator.create_image(data_other)


stopwatch = StopWatch()
for (i, (vocal, drums, bass, piano, other)) in enumerate(
    zip(image_vocal, image_drums, image_bass, image_piano, image_other)
):
    with stopwatch:
        vocal = to_transparent_bg(vocal)
        drums = to_transparent_bg(drums)
        bass = to_transparent_bg(bass)
        piano = to_transparent_bg(piano)
        other = to_transparent_bg(other)

        colorized_vocal = image_tint(vocal, '#0000FF')
        colorized_drums = image_tint(drums, '#FF0000')
        colorized_bass = image_tint(bass, '#00FF00')
        colorized_piano = image_tint(piano, '#000000')
        colorized_other = image_tint(other, '#FF00FF')

        merged_image = merge_images(
            merge_images(
                merge_images(merge_images(colorized_drums, colorized_vocal), colorized_bass),
                colorized_piano,
            ),
            colorized_other,
        )
        final_image = Image.new('RGB', merged_image.size, "BLACK")
        final_image.paste(merged_image, (0, 0), merged_image)
        final_image.save(f'{BASE_FOLDER}/{i}.png')
    print(f'{i} generated in {stopwatch.interval}')
