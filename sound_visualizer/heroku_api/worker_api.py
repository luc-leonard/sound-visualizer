import io
import json
import logging
import random
from typing import Dict

from google.cloud import pubsub_v1
from google.cloud.storage.client import Client as CloudStorageClient

from sound_visualizer.app.input import SoundReader
from sound_visualizer.app.output.grey_scale_image import GreyScaleImageGenerator
from sound_visualizer.app.sound import SpectralAnalyzer
from sound_visualizer.utils.logger import init_logger

logger = logging.getLogger(__name__)

log_levels: Dict[str, str] = {'google.cloud.pubsub_v1.subscriber._protocol.leaser': 'INFO'}


def download_file(bucket_filename, local_filename):
    bucket.blob(bucket_filename).download_to_filename(local_filename)


def callback(message):
    data = json.loads(message.data)
    logger.info(data)
    filename = '/tmp/' + str(random.randint(0, 255))

    bucket.blob(data['filename']).download_to_filename(filename)

    del data['filename']
    sound_reader = SoundReader(filename=filename, **data)
    spectral_analyser = SpectralAnalyzer(frame_size=4096, overlap_factor=0.6)
    spectral_analysis = spectral_analyser.get_spectrogram_data(sound_reader)
    image = GreyScaleImageGenerator(border_width=10, border_color='red').create_image(
        spectral_analysis.fft_data
    )
    with io.BytesIO() as bytes:
        image.save(bytes, format='png')
        bytes.seek(0)
        bucket.blob(data['result_id'] + '.png').upload_from_file(bytes)
    message.ack()


if __name__ == '__main__':
    init_logger()
    for (logger_name, log_level) in log_levels.items():
        logging.getLogger(logger_name).setLevel(log_level)
    storage_client = CloudStorageClient()
    bucket = storage_client.bucket('spectrogram-images')

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path('luc-leonard-sound-visualizer', 'my-sub')
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result()
        except TimeoutError as e:
            streaming_pull_future.cancel()
            logger.warning(f'timeout due to {e}')
