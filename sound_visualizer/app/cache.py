import os
import typing as t
from pathlib import Path

from pydantic import BaseModel


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
