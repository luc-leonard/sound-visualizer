import io
import json
import logging
import random

import numpy as np
import PIL
import pymongo
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from sound_visualizer.app.converter import Mp3Converter
from sound_visualizer.app.downloader.youtube import YoutubeDownloader
from sound_visualizer.app.image.grey_scale_image_generator import GreyScaleImageGenerator
from sound_visualizer.app.message_queue.google_cloud_pubsub import GoogleCloudConsumer
from sound_visualizer.app.sound import SpectralAnalyzer
from sound_visualizer.app.sound.sound_reader import SoundReader
from sound_visualizer.app.storage.google_cloud_storage import GoogleCloudStorage
from sound_visualizer.config import config_from_env
from sound_visualizer.models.spectral_analysis_request import (
    SpectralAnalysisFlow,
    SpectralAnalysisFlowORM,
)
from sound_visualizer.utils import StopWatch
from sound_visualizer.utils.logger import init_logger

logger = logging.getLogger(__name__)


def download_file(bucket_filename, local_filename):
    with open(local_filename, 'wb') as f:
        storage.download_to(bucket_filename, f)


def vstack(images):
    if len(images) == 0:
        raise ValueError("Need 0 or more images")

    if isinstance(images[0], np.ndarray):
        images = [Image.fromarray(img) for img in images]
    width = max([img.size[0] for img in images])
    height = sum([img.size[1] for img in images])
    stacked = Image.new(images[0].mode, (width, height))

    y_pos = 0
    for img in images:
        stacked.paste(img, (0, y_pos))
        y_pos += img.size[1]
    return stacked


def toLogScale(image: PIL.Image, frequency_domain: np.ndarray) -> PIL.Image:
    cut_offs = [0, 5000, 15000, 100000]
    idx_cutoffs = [frequency_domain.searchsorted(frequency) for frequency in cut_offs]

    images = [
        image.copy()
        .crop((0, image.height - upper_frequency, image.width, image.height - lower_frequency))
        .resize((image.width, idx_cutoffs[1]))
        for (lower_frequency, upper_frequency) in zip(idx_cutoffs, idx_cutoffs[1:])
    ]

    return vstack(list(reversed(images)))


def generate_image(request: SpectralAnalysisFlow) -> Image:
    stopwatch = StopWatch()
    orm.update_request_status(request.id, 'downloading')
    if request.parameters.youtube_url is not None and len(request.parameters.youtube_url) == 0:
        filename = '/tmp/' + str(random.randint(0, 255))
        with stopwatch:
            download_file(request.parameters.filename, filename)
        logger.info(f"downloaded {request.parameters.filename} in {stopwatch.interval}s")
    else:
        with stopwatch:
            filename = YoutubeDownloader().download(request.parameters.youtube_url)
        orm.add_stopwatch(request.id, 'download', stopwatch.interval)
    with stopwatch:
        orm.update_request_status(request.id, 'converting')
        wav_filename = Mp3Converter(filename=filename).convert()
    orm.add_stopwatch(request.id, 'convert', stopwatch.interval)
    logger.info(f"converted {filename} to {wav_filename} in {stopwatch.interval}s")
    orm.update_request_status(request.id, 'analysing')

    sound_reader = SoundReader(
        filename=wav_filename,
        start_second=request.parameters.start_second,
        length_second=request.parameters.length_second,
    )
    spectral_analyser = SpectralAnalyzer(
        frame_size=2 ** request.parameters.frame_size_power,
        overlap_factor=request.parameters.overlap_factor,
    )
    with stopwatch:
        spectral_analysis = spectral_analyser.get_spectrogram_data(sound_reader)
    orm.add_stopwatch(request.id, 'fft_computation', stopwatch.interval)
    # orm.add_memory_used(request.id, 'fft_data', spectral_analysis.fft_data.nbytes)
    orm.update_request_status(request.id, 'generating image...')
    logger.info(f'generated fft data {spectral_analysis}')
    with stopwatch:
        image = GreyScaleImageGenerator(border_width=15, border_color='black').create_image(
            spectral_analysis
        )

        ImageFont.load_default()
        draw = ImageDraw.Draw(image)
        for i in range(0, int(np.floor(spectral_analysis.time_domain[-1])), 1):
            second_idx = spectral_analysis.time_domain.searchsorted(i)
            draw.line([(0, second_idx), (15, second_idx)], fill='red', width=1)
            if i % 5 == 0:
                draw.text(xy=(0, second_idx + 16), text=f'{i}', fill='red')

        for j in [10, 100, 1000, 10000]:
            frequency_idx = spectral_analysis.frequency_domain.searchsorted(j)
            draw.line(
                [(frequency_idx + 15, 0), (frequency_idx + 15, image.size[1])], fill='red', width=1
            )

        image = ImageEnhance.Contrast(image).enhance(5.0)
        image = image.rotate(90, expand=True)
        image = toLogScale(image, spectral_analysis.frequency_domain)
    orm.add_stopwatch(request.id, 'image generation', stopwatch.interval)
    return image


def callback(message):
    try:
        data = json.loads(message.data)
        request = SpectralAnalysisFlow(**data)
        logger.info(f'request = {request}')
        orm.update_request_status(request.id, 'beginning')
        image = generate_image(request)
        orm.save_image_size(request.id, image.size)
        with io.BytesIO() as bytes:
            image.save(bytes, format='png')
            bytes.seek(0)
            orm.update_request_status(request.id, 'uploading image')
            storage.upload_from(request.id, bytes)
            orm.update_request_status(request.id, 'finished')
            db.results.insert_one({'source': request.dict(), 'result': request.id})
        message.ack()
    except Exception as e:
        logger.error('error handling message', exc_info=e)
        message.ack()
    finally:
        message.ack()


config = config_from_env()
client = pymongo.MongoClient(config.mongo_connection_string)
db = client.sound_visualizer
orm = SpectralAnalysisFlowORM(db)

if __name__ == '__main__':
    init_logger()

    storage = GoogleCloudStorage(config.google_storage_bucket_name)
    subscriber = GoogleCloudConsumer(config.google_application_project_name)
    streaming_pull_future = subscriber.consume('my-sub', callback=callback)
    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError as e:
            streaming_pull_future.cancel()
            logger.warning(f'timeout due to {e}')
