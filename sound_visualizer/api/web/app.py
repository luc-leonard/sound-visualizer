import pymongo
from flask import Flask
from google.cloud import pubsub_v1
from google.cloud.storage.client import Client as CloudStorageClient

from sound_visualizer.api.config import config_from_env
from sound_visualizer.app.cache import Cache


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_storage_client():
    return CloudStorageClient()


def get_bucket(storage_client, bucket_name):
    return storage_client.bucket(bucket_name)


def get_topic_path(publisher):
    return publisher.topic_path('luc-leonard-sound-visualizer', 'my-topic')


config = config_from_env()


class MyApp(Flask):
    config = config_from_env()
    cache = Cache(cache_folder='/tmp/sound_visualizer')
    publisher = get_publisher_client()
    storage_client = get_storage_client()
    bucket = get_bucket(storage_client, config.google_storage_bucket_name)
    topic_path = get_topic_path(publisher)
    client = pymongo.MongoClient(config.mongo_connection_string)
    db = client.sound_visualizer
