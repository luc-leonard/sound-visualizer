import logging

from PIL import Image, ImageOps

from sound_visualizer.app.image.grey_scale_image_generator import GreyScaleImageGenerator
from sound_visualizer.app.sound import SoundReader, SpectralAnalyzer


def merge_images(img1: Image.Image, img2: Image.Image) -> Image.Image:
    newimg1 = Image.new('RGBA', size=img1.size, color=(0, 0, 0, 0))
    newimg1.paste(img2, (0, 0))
    newimg1.paste(img1, (0, 0))

    # paste img2 on top of img1
    newimg2 = Image.new('RGBA', size=img1.size, color=(0, 0, 0, 0))
    newimg2.paste(img1, (0, 0))
    newimg2.paste(img2, (0, 0))

    # blend with alpha=0.5
    return Image.blend(newimg1, newimg2, alpha=0.5)


def to_transparent_bg(image: Image.Image) -> Image.Image:
    image.putalpha(image.copy().convert('L'))
    return image


def image_tint(src, color="#FFFFFF"):
    gray, alpha = src.split()
    result = ImageOps.colorize(gray, (0, 0, 0, 0), color)
    result.putalpha(alpha)
    return result


logging.getLogger().setLevel('DEBUG')

analyser = SpectralAnalyzer(overlap_factor=0.75, frame_size=2 ** 12)
image_generator = GreyScaleImageGenerator(border_width=0)

data_vocal = analyser.get_spectrogram_data(
    SoundReader(
        filename='/home/lleonard/dev/perso/sound-visualizer/spleets/headroom/audio_headroom/vocals.wav'
    )
)
data_drums = analyser.get_spectrogram_data(
    SoundReader(
        filename='/home/lleonard/dev/perso/sound-visualizer/spleets/headroom/audio_headroom/drums.wav'
    )
)
data_bass = analyser.get_spectrogram_data(
    SoundReader(
        filename='/home/lleonard/dev/perso/sound-visualizer/spleets/headroom/audio_headroom/bass.wav'
    )
)
data_piano = analyser.get_spectrogram_data(
    SoundReader(
        filename='/home/lleonard/dev/perso/sound-visualizer/spleets/headroom/audio_headroom/piano.wav'
    )
)
data_other = analyser.get_spectrogram_data(
    SoundReader(
        filename='/home/lleonard/dev/perso/sound-visualizer/spleets/headroom/audio_headroom/other.wav'
    )
)


image_vocal = image_generator.create_image(data_vocal)
image_drums = image_generator.create_image(data_drums)
image_bass = image_generator.create_image(data_bass)
image_piano = image_generator.create_image(data_piano)
image_other = image_generator.create_image(data_other)

for (i, (vocal, drums, bass, piano, other)) in enumerate(
    zip(image_vocal, image_drums, image_bass, image_piano, image_other)
):
    vocal = to_transparent_bg(vocal)
    drums = to_transparent_bg(drums)
    bass = to_transparent_bg(bass)
    piano = to_transparent_bg(piano)
    other = to_transparent_bg(other)

    colorized_vocal = image_tint(vocal, '#0000FF')
    colorized_drums = image_tint(drums, '#FF0000')
    colorized_bass = image_tint(bass, '#00FF00')
    colorized_piano = image_tint(piano, '#AAFF00')
    colorized_other = image_tint(other, '#00FFAA')

    colorized_vocal.save(f'vocal_{i}.png')
    colorized_drums.save(f'drums_{i}.png')
    colorized_bass.save(f'bass_{i}.png')
    colorized_piano.save(f'piano_{i}.png')
    colorized_other.save(f'other_{i}.png')
    merge_images(
        merge_images(
            merge_images(merge_images(colorized_drums, colorized_vocal), colorized_bass),
            colorized_piano,
        ),
        colorized_other,
    ).save(f'{i}.png')
    # Image.merge('RGB', (vocal.convert('L'), accomp.convert('L'), Image.new('L',(vocal.width, vocal.height)))).save(f'{i}.png')
    # ImageChops.darker(colorized_vocal, colorized_accomp)
    print(f'{i}')
