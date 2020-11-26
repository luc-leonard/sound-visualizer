import pymongo
from flask import Flask

from sound_visualizer.api.config import config_from_env
from sound_visualizer.app.cache import Cache
from sound_visualizer.app.message_queue.google_cloud_pubsub import GoogleCloudPublisher
from sound_visualizer.app.storage.google_cloud_storage import GoogleCloudStorage

config = config_from_env()


class MyApp(Flask):
    config = config_from_env()
    cache = Cache(cache_folder='/tmp/sound_visualizer')
    publisher = GoogleCloudPublisher(config.google_application_project_name)
    storage = GoogleCloudStorage(config.google_storage_bucket_name)
    client = pymongo.MongoClient(config.mongo_connection_string)
    db = client.sound_visualizer
