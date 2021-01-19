import io
import os
import typing as t
from pathlib import Path

from pydantic import BaseModel

from sound_visualizer.common.storage.storage import Storage


class Cache(BaseModel):
    cache_folder: Path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.makedirs(self.cache_folder, exist_ok=True)

    def _get_data_path(self, data_id: str) -> Path:
        return self.cache_folder / data_id

    def is_data_in_cache(self, data_id: str) -> bool:
        return self._get_data_path(data_id).exists()

    def get_data_in_cache(self, data_id: str) -> t.BinaryIO:
        return open(self._get_data_path(data_id), mode='rb')

    def put_data_in_cache(self, data_id: str, data: t.BinaryIO):
        file = open(self._get_data_path(data_id), mode='wb')
        return file.write(data.read())


class CachedStorage:
    def __init__(self, cache: Cache, storage: Storage):
        self.cache = cache
        self.storage = storage

    def get(self, data_id: str) -> t.BinaryIO:
        if self.cache.is_data_in_cache(data_id):
            return self.cache.get_data_in_cache(data_id)
        else:
            data = io.BytesIO()
            self.storage.download_to(data_id, data)
            data.seek(0)
            self.cache.put_data_in_cache(data_id, data)
            data.seek(0)
            return data
