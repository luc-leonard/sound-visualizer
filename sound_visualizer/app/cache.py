import io
import os
import typing as t
from pathlib import Path

from pydantic import BaseModel


class Cache(BaseModel):
    cache_folder: Path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.makedirs(self.cache_folder, exist_ok=True)

    def _get_result_path(self, result_id: str) -> Path:
        return self.cache_folder / result_id

    def is_result_in_cache(self, result_id: str) -> bool:
        return self._get_result_path(result_id).exists()

    def get_result_in_cache(self, result_id: str) -> t.BinaryIO:
        return open(self._get_result_path(result_id), mode='rb')

    def put_result_in_cache(self, result_id: str, data: io.BytesIO):
        file = open(self._get_result_path(result_id), mode='wb')
        return file.write(data.read())
