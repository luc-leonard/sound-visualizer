import pymongo
from flask import Flask
from google.cloud import pubsub_v1
from google.cloud.storage.client import Client as CloudStorageClient

from sound_visualizer.heroku_api.config import config_from_env


def get_publisher_client():
    return pubsub_v1.PublisherClient()


def get_storage_client():
    return CloudStorageClient()


def get_bucket(storage_client):
    return storage_client.bucket('spectrogram-images')


def get_topic_path(publisher):
    return publisher.topic_path('luc-leonard-sound-visualizer', 'my-topic')


config = config_from_env()


class MyApp(Flask):
    publisher = get_publisher_client()
    storage_client = get_storage_client()
    bucket = get_bucket(storage_client)
    topic_path = get_topic_path(publisher)
    config = config_from_env()
    client = pymongo.MongoClient(
        f"mongodb+srv://{config.mongo_username}:{config.mongo_password}@cluster0.tucaz.mongodb.net/sound-visualizer?retryWrites=true&w=majority"
    )
    db = client.sound_visualizer
