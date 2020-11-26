import pymongo
from flask import Flask

from sound_visualizer.app.cache import Cache
from sound_visualizer.app.message_queue.google_cloud_pubsub import GoogleCloudPublisher
from sound_visualizer.app.storage.google_cloud_storage import GoogleCloudStorage
from sound_visualizer.config import config_from_env
from sound_visualizer.models.spectral_analysis_request import SpectralAnalysisRequestORM
from sound_visualizer.utils.logger import init_logger

config = config_from_env()


class MyApp(Flask):
    config = config_from_env()
    cache = Cache(cache_folder='/tmp/sound_visualizer')
    publisher = GoogleCloudPublisher(config.google_application_project_name)
    storage = GoogleCloudStorage(config.google_storage_bucket_name)
    client = pymongo.MongoClient(config.mongo_connection_string)
    db = client.sound_visualizer
    orm = SpectralAnalysisRequestORM(db)


def create_app(name):
    app = MyApp(name)
    # api = Api(app)
    return app


init_logger()
app = create_app(__name__)
