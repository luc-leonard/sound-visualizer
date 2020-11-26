import typing

from google.cloud.storage.client import Client

from sound_visualizer.app.storage.storage import Storage


class GoogleCloudStorage(Storage):
    def __init__(self, bucket_name):
        storage_client = Client()
        self.bucket = storage_client.bucket(bucket_name)

    def download_to(self, filename: str, to: typing.BinaryIO):
        self.bucket.blob(filename).download_to_file(to)
        to.seek(0)

    def upload_from(self, filename: str, _from: typing.BinaryIO):
        self.bucket.blob(filename).upload_from_file(_from)
        _from.seek(0)
