import json
import logging

import pymongo
import requests
from bs4 import BeautifulSoup

from sound_visualizer.common.converter.FFMPEGConverter import FFMPEGConverter
from sound_visualizer.common.downloader.youtube import YoutubeDownloader
from sound_visualizer.common.message_queue.rabbitmq import (
    RabbitMqConsumer,
    RabbitMqPublisher,
    make_connection,
    make_parameters,
)
from sound_visualizer.common.storage.google_cloud_storage import GoogleCloudStorage
from sound_visualizer.config import config_from_env
from sound_visualizer.models.spectral_analysis_request import (
    SpectralAnalysisFlow,
    SpectralAnalysisFlowORM,
)
from sound_visualizer.utils import StopWatch
from sound_visualizer.utils.logger import init_logger

logger = logging.getLogger(__name__)


def save_youtube_title(request: SpectralAnalysisFlow):
    assert request.parameters.youtube_url is not None
    youtube_page = requests.get(request.parameters.youtube_url)
    parsed_page = BeautifulSoup(youtube_page.text, 'html.parser')
    orm.save_title(request.id, parsed_page.title.text)


def download_sound(request: SpectralAnalysisFlow) -> None:
    stopwatch = StopWatch()
    orm.update_request_status(request.id, 'downloading')
    with stopwatch:
        filename = YoutubeDownloader().download(request.parameters.youtube_url)
        save_youtube_title(request)
    orm.add_stopwatch(request.id, 'download', stopwatch.interval)

    with stopwatch:
        orm.update_request_status(request.id, 'converting')
        mp3_filename = FFMPEGConverter(filename=filename).convert('mp3')
    orm.add_stopwatch(request.id, 'convert', stopwatch.interval)
    logger.info(f"converted {filename} to {mp3_filename} in {stopwatch.interval}s")
    orm.update_request_status(request.id, 'uploading sound')
    with open(mp3_filename, 'rb') as file:
        storage.upload_from(request.id, file)


def callback(message):
    message.ack()
    try:
        data = json.loads(message.data)
        request = SpectralAnalysisFlow(**data)
        logger.info(f'request = {request}')
        orm.update_request_status(request.id, 'beginning')
        download_sound(request)

        def _publish():
            publisher.publish('uploaded-sound', request.json().encode('utf-8'))

        publisher.channel.connection.add_callback_threadsafe(_publish)
    except Exception as e:
        logger.error('error handling message', exc_info=e)


config = config_from_env()
client = pymongo.MongoClient(config.mongo_connection_string)
db = client.sound_visualizer
orm = SpectralAnalysisFlowORM(db)

if __name__ == '__main__':
    init_logger()

    storage = GoogleCloudStorage('sound_analyser-sounds')
    connection = make_connection(config)
    # two connections are needed since we cannot share them across threads.
    subscriber = RabbitMqConsumer(connection)
    publisher = RabbitMqPublisher(connection, make_parameters(config))

    streaming_pull_future = subscriber.consume('render-request', callback=callback)
    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError as e:
            streaming_pull_future.cancel()
            logger.warning(f'timeout due to {e}')
