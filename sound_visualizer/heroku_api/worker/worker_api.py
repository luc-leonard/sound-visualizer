import io
import json
import logging
import random
from typing import Optional

from google.cloud import pubsub_v1
from google.cloud.storage.client import Client as CloudStorageClient
from PIL import Image, ImageEnhance
from pydantic import BaseModel

from sound_visualizer.app.input import SoundReader
from sound_visualizer.app.input.converter import Mp3Converter
from sound_visualizer.app.input.downloader.youtube import YoutubeDownloader
from sound_visualizer.app.output.grey_scale_image import GreyScaleImageGenerator
from sound_visualizer.app.sound import SpectralAnalyzer
from sound_visualizer.utils import StopWatch
from sound_visualizer.utils.logger import init_logger

logger = logging.getLogger(__name__)


class SpectrogramRequestData(BaseModel):
    # one, or the other
    youtube_url: Optional[str]
    filename: Optional[str]

    start_second: Optional[int] = 0
    length_second: Optional[int] = -1
    overlap_factor: Optional[float] = 0.6


def download_file(bucket_filename, local_filename):
    bucket.blob(bucket_filename).download_to_filename(local_filename)


def generate_image(request: SpectrogramRequestData) -> Image:
    stopwatch = StopWatch()
    if request.youtube_url is not None and len(request.youtube_url) == 0:
        filename = '/tmp/' + str(random.randint(0, 255))
        with stopwatch:
            bucket.blob(request.filename).download_to_filename(filename)
        logger.info(f"downloaded {request.filename} in {stopwatch.interval}s")
    else:
        filename = YoutubeDownloader().download(request.youtube_url)
    with stopwatch:
        wav_filename = Mp3Converter(filename=filename).convert()
    logger.info(f"converted {filename} to {wav_filename} in {stopwatch.interval}s")
    sound_reader = SoundReader(
        filename=wav_filename,
        start_second=request.start_second,
        length_second=request.length_second,
    )
    spectral_analyser = SpectralAnalyzer(frame_size=4096, overlap_factor=request.overlap_factor)
    spectral_analysis = spectral_analyser.get_spectrogram_data(sound_reader)
    return ImageEnhance.Contrast(
        GreyScaleImageGenerator(border_width=10, border_color='red').create_image(
            spectral_analysis.fft_data
        )
    ).enhance(10.0)


def callback(message):

    try:
        data = json.loads(message.data)
        request = SpectrogramRequestData(**data)
        logger.info(f'request = {request}')

        image = generate_image(request)
        with io.BytesIO() as bytes:
            image.save(bytes, format='png')
            bytes.seek(0)
            bucket.blob(data['result_id'] + '.png').upload_from_file(bytes)
    except Exception as e:
        logger.error('error handling message', e)
    finally:
        message.ack()


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
