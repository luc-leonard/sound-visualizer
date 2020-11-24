import io
import json
import logging
import random

import pymongo
from google.cloud import pubsub_v1
from google.cloud.storage.client import Client as CloudStorageClient
from PIL import Image, ImageEnhance

from sound_visualizer.app.input import SoundReader
from sound_visualizer.app.input.converter import Mp3Converter
from sound_visualizer.app.input.downloader.youtube import YoutubeDownloader
from sound_visualizer.app.output.grey_scale_image import GreyScaleImageGenerator
from sound_visualizer.app.sound import SpectralAnalyzer
from sound_visualizer.heroku_api.config import config_from_env
from sound_visualizer.heroku_api.models.spectrogram_request_data import SpectrogramRequestData
from sound_visualizer.utils import StopWatch
from sound_visualizer.utils.logger import init_logger

logger = logging.getLogger(__name__)


def download_file(bucket_filename, local_filename):
    bucket.blob(bucket_filename).download_to_filename(local_filename)


def generate_image(request: SpectrogramRequestData) -> Image:
    stopwatch = StopWatch()
    db.status.insert_one({'request_id': request.result_id, 'stage': 'downloading'})
    if request.youtube_url is not None and len(request.youtube_url) == 0:
        filename = '/tmp/' + str(random.randint(0, 255))
        with stopwatch:
            bucket.blob(request.filename).download_to_filename(filename)
        logger.info(f"downloaded {request.filename} in {stopwatch.interval}s")
    else:
        filename = YoutubeDownloader().download(request.youtube_url)
    with stopwatch:
        db.status.insert_one({'request_id': request.result_id, 'stage': 'converting'})
        wav_filename = Mp3Converter(filename=filename).convert()
    db.status.insert_one({'request_id': request.result_id, 'stage': 'analysing...'})
    logger.info(f"converted {filename} to {wav_filename} in {stopwatch.interval}s")
    sound_reader = SoundReader(
        filename=wav_filename,
        start_second=request.start_second,
        length_second=request.length_second,
    )
    spectral_analyser = SpectralAnalyzer(
        frame_size=2 ** request.frame_size_power, overlap_factor=request.overlap_factor
    )
    spectral_analysis = spectral_analyser.get_spectrogram_data(sound_reader)
    db.status.insert_one(
        {'request_id': request.result_id, 'stage': 'generating image... almost done...'}
    )
    logger.info(f'generated fft data {spectral_analysis}')
    image = ImageEnhance.Contrast(
        GreyScaleImageGenerator(border_width=10, border_color='red').create_image(
            spectral_analysis.fft_data
        )
    ).enhance(10.0)
    return image


def callback(message):
    try:
        data = json.loads(message.data)
        request = SpectrogramRequestData(**data)
        logger.info(f'request = {request}')
        db.status.insert_one({'request_id': request.result_id, 'stage': 'beginning'})
        image = generate_image(request)
        with io.BytesIO() as bytes:
            image.save(bytes, format='png')
            bytes.seek(0)
            db.status.insert_one({'request_id': request.result_id, 'stage': 'uploading'})
            bucket.blob(data['result_id'] + '.png').upload_from_file(bytes)
            db.status.insert_one({'request_id': request.result_id, 'stage': 'finished'})
            db.results.insert_one({'source': request.dict(), 'result': request.result_id})
        message.ack()
    except Exception as e:
        logger.error('error handling message', e)


config = config_from_env()
client = pymongo.MongoClient(
    f"mongodb+srv://{config.mongo_username}:{config.mongo_password}@cluster0.tucaz.mongodb.net/sound-visualizer?retryWrites=true&w=majority"
)
db = client.sound_visualizer

if __name__ == '__main__':
    init_logger()

    storage_client = CloudStorageClient()
    bucket = storage_client.bucket('spectrogram-images')

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path('luc-leonard-sound-visualizer', 'my-sub')
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError as e:
            streaming_pull_future.cancel()
            logger.warning(f'timeout due to {e}')
