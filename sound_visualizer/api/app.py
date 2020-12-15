import logging

import pymongo
from flask import Flask, send_file
from flask_cors import CORS
from flask_restful import Api

from sound_visualizer.api.resources.spectral_analysis_request import (
    SpectralAnalysisRequestListResource,
    SpectralAnalysisRequestResource,
)
from sound_visualizer.api.resources.spectral_analysis_result import SpectralAnalysisResultResource
from sound_visualizer.api.resources.tiles_resource import TilesResources
from sound_visualizer.app.cache import Cache
from sound_visualizer.app.message_queue.google_cloud_pubsub import GoogleCloudPublisher
from sound_visualizer.app.spectral_analysis_request_handler import SpectralAnalysisRequestHandler
from sound_visualizer.app.storage.google_cloud_storage import GoogleCloudStorage
from sound_visualizer.config import config_from_env
from sound_visualizer.models.spectral_analysis_request import SpectralAnalysisFlowORM
from sound_visualizer.utils.logger import init_logger

logger = logging.getLogger(__name__)


class MyApp(Flask):
    the_config = config_from_env()
    cache = Cache(cache_folder='/tmp/sound_visualizer')
    publisher = GoogleCloudPublisher(the_config.google_application_project_name)
    storage = GoogleCloudStorage(the_config.google_storage_bucket_name)
    client = pymongo.MongoClient(the_config.mongo_connection_string)
    db = client.sound_visualizer
    orm = SpectralAnalysisFlowORM(db)


def create_app(name):
    import os

    logger.info(f'CURRENT PATH = {os.getcwd()}')
    app = MyApp(name, static_folder=f'{os.getcwd()}/static', static_url_path='/www/')
    logger.info(app.the_config)
    api = Api(app)
    if app.the_config.cors_origin is not None:
        CORS(app, resources={r"/*": {"origins": app.the_config.cors_origin}})

    handler = SpectralAnalysisRequestHandler(app.orm, app.publisher, app.storage)

    api.add_resource(
        SpectralAnalysisRequestListResource(handler),
        '/requests/',
    )
    api.add_resource(SpectralAnalysisRequestResource(handler), '/request/<string:analysis_id>')

    api.add_resource(
        SpectralAnalysisResultResource(storage=app.storage, cache=app.cache, orm=app.orm),
        '/result/<string:analysis_id>',
    )
    api.add_resource(
        TilesResources(storage=app.storage, cache=app.cache),
        '/tiles/<string:result_id>/<int:x>.png',
    )
    return app


init_logger()
app = create_app(__name__)


@app.route('/')
def home():
    return send_file('../../static/dist/index.html')


@app.after_request
def add_headers(response):
    for hdr_name in list(response.headers.keys()):
        if hdr_name.startswith('Access-Control-'):
            response.headers.remove(hdr_name)
    return response
