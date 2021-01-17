import io
import json
import logging
from typing import Generator

import numpy as np
import PIL
import pymongo
import requests
from bs4 import BeautifulSoup
from PIL import Image
from spleeter.separator import Separator

from sound_visualizer.app.converter import FFMPEGConverter
from sound_visualizer.app.image.grey_scale_image_generator import GreyScaleImageGenerator
from sound_visualizer.app.message_queue.rabbitmq import RabbitMqConsumer, make_connection
from sound_visualizer.app.sound import SpectralAnalyzer
from sound_visualizer.app.sound.sound_reader import SoundReader
from sound_visualizer.app.storage.google_cloud_storage import GoogleCloudStorage
from sound_visualizer.config import config_from_env
from sound_visualizer.models.spectral_analysis_request import (
    SpectralAnalysisFlow,
    SpectralAnalysisFlowORM,
)
from sound_visualizer.utils import StopWatch
from sound_visualizer.utils.google_cloud import init_google_cloud
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


def toLogScale(image: PIL.Image, frequency_domain: np.ndarray) -> PIL.Image.Image:
    cut_offs = [0, 5000, 15000, 100000]
    idx_cutoffs = [frequency_domain.searchsorted(frequency) for frequency in cut_offs]

    images = [
        image.copy()
        .crop((0, image.height - upper_frequency, image.width, image.height - lower_frequency))
        .resize((image.width, idx_cutoffs[1]))
        for (lower_frequency, upper_frequency) in zip(idx_cutoffs, idx_cutoffs[1:])
    ]

    return vstack(list(reversed(images)))


def save_youtube_title(request: SpectralAnalysisFlow):
    assert request.parameters.youtube_url is not None
    youtube_page = requests.get(request.parameters.youtube_url)
    parsed_page = BeautifulSoup(youtube_page.text, 'html.parser')
    orm.save_title(request.id, parsed_page.title.text)


def generate_image(request: SpectralAnalysisFlow) -> Generator[PIL.Image.Image, None, None]:
    stopwatch = StopWatch()

    mp3_filename = '/tmp/' + request.id
    with open(mp3_filename, 'wb') as f:
        sound_storage.download_to(request.id, f)

    with stopwatch:
        wav_filename = FFMPEGConverter(filename=mp3_filename).convert('wav')
    orm.add_stopwatch(request.id, 'convert', stopwatch.interval)
    logger.info(f"converted {mp3_filename} to {wav_filename} in {stopwatch.interval}s")

    orm.update_request_status(request.id, 'splitting')
    sound_reader = SoundReader(filename=wav_filename)

    # separated = separator.separate(sound_reader.get_data().data, sound_reader.get_data().sample_rate)
    orm.update_request_status(request.id, 'analysing')

    spectral_analyser = SpectralAnalyzer(
        frame_size=2 ** request.parameters.frame_size_power,
        overlap_factor=request.parameters.overlap_factor,
    )

    with stopwatch:
        spectral_analysis = spectral_analyser.get_spectrogram_data(sound_reader)
    orm.add_stopwatch(request.id, 'fft_computation', stopwatch.interval)
    orm.save_duration(request.id, spectral_analysis.time_domain[-1])
    orm.update_request_status(request.id, 'generating image...')
    logger.info(f'generated fft data {spectral_analysis}')
    images = GreyScaleImageGenerator(border_width=15, border_color='black').create_image(
        spectral_analysis
    )
    orm.add_stopwatch(request.id, 'image generation', stopwatch.interval)
    return images


def callback(message):
    message.ack()
    try:
        data = json.loads(message.data)
        request = SpectralAnalysisFlow(**data)
        logger.info(f'request = {request}')
        orm.update_request_status(request.id, 'beginning')
        images = generate_image(request)
        width = 0
        for (idx, image) in enumerate(images):
            height = image.height
            width += image.width
            if idx == 0:
                orm.save_tile_size(request.id, image.width)
            with io.BytesIO() as bytes:
                image.save(bytes, format='png')
                bytes.seek(0)
                orm.update_request_status(request.id, f'uploading image {idx}')
                storage.upload_from(f'{request.id}_{idx}', bytes)
        orm.update_request_status(request.id, 'finished')
        orm.save_image_size(request.id, (width, height))
    except Exception as e:
        logger.error('error handling message', exc_info=e)


config = config_from_env()
client = pymongo.MongoClient(config.mongo_connection_string)
db = client.sound_visualizer
orm = SpectralAnalysisFlowORM(db)

if __name__ == '__main__':
    init_logger()
    init_google_cloud(config)
    connection = make_connection(config)
    sound_storage = GoogleCloudStorage('sound_analyser-sounds')
    storage = GoogleCloudStorage(config.google_storage_bucket_name)
    subscriber = RabbitMqConsumer(connection)
    separator = Separator('spleeter:5stems')
    streaming_pull_future = subscriber.consume('uploaded-sound', callback=callback)
    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError as e:
            streaming_pull_future.cancel()
            logger.warning(f'timeout due to {e}')
