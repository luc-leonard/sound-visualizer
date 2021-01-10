import logging
import os
import time
from pathlib import Path

import pika
import pymongo
from flask import Flask, send_file
from flask_cors import CORS
from flask_restful import Api

from sound_visualizer.api.resources.spectral_analysis_request import (
    SpectralAnalysisRequestListResource,
    SpectralAnalysisRequestResource,
)
from sound_visualizer.api.resources.tiles_resource import TilesResources
from sound_visualizer.app.cache import Cache
from sound_visualizer.app.message_queue.rabbitmq import RabbitMqPublisher, make_connection
from sound_visualizer.app.spectral_analysis_request_handler import SpectralAnalysisRequestHandler
from sound_visualizer.app.storage.google_cloud_storage import GoogleCloudStorage
from sound_visualizer.config import config_from_env
from sound_visualizer.models.spectral_analysis_request import SpectralAnalysisFlowORM
from sound_visualizer.utils.google_cloud import init_google_cloud
from sound_visualizer.utils.logger import init_logger

logger = logging.getLogger(__name__)

init_logger()


def heartbeat(connection: pika.BlockingConnection):
    while True:
        time.sleep(15)
        # it is likely that a better way exists
        connection.channel().close()


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.the_config = config_from_env()
        init_google_cloud(self.the_config)
        self.cache = Cache(cache_folder='/tmp/sound_visualizer')
        connection = make_connection(self.the_config)

        self.publisher = RabbitMqPublisher(connection)
        self.storage = GoogleCloudStorage(self.the_config.google_storage_bucket_name)
        client = pymongo.MongoClient(self.the_config.mongo_connection_string)
        db = client.sound_visualizer
        self.orm = SpectralAnalysisFlowORM(db)


def create_app(name):
    logger.info(f'CURRENT PATH = {os.getcwd()}')
    app = MyApp(name)
    api = Api(app)
    if app.the_config.cors_origin is not None:
        CORS(app, resources={r"/*": {"origins": app.the_config.cors_origin.split(';')}})

    handler = SpectralAnalysisRequestHandler(app.orm, app.publisher, app.storage)

    api.add_resource(
        SpectralAnalysisRequestListResource(handler),
        '/requests/',
    )
    api.add_resource(SpectralAnalysisRequestResource(handler), '/request/<string:analysis_id>')

    api.add_resource(
        TilesResources(storage=app.storage, cache=app.cache),
        '/tiles/<string:result_id>/<int:x>.png',
    )
    logger.info('CREATED APP')
    return app


app = create_app(__name__)


# catch all URL. allows us to use Vue router history
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path: str):
    logger.info(f'{path} asked. we are at {os.getcwd()}')
    base_path = os.getcwd()
    if 'api' in base_path:
        base_path = base_path + '../../'
    full_path = Path(base_path) / 'static/dist' / path
    if full_path.exists() and not full_path.is_dir():
        return send_file(f'{base_path}/static/dist/' + path)
    else:
        logger.warning(
            f'{path} not found. It usually means that path is for the frontend, and that we should send the index'
        )
        # it means the 'path' is for the frontend :)
        return send_file(f'{base_path}/static/dist/index.html')


@app.after_request
def add_headers(response):
    for hdr_name in list(response.headers.keys()):
        if hdr_name.startswith('Access-Control-'):
            response.headers.remove(hdr_name)
    return response


if __name__ == '__main__':
    app.run()
