import io
import logging
import typing
from pathlib import Path

import PIL.Image

from sound_visualizer.app.cache import Cache, CachedStorage
from sound_visualizer.app.storage.storage import Storage

logger = logging.getLogger(__name__)


class HorizontalTiler:
    def __init__(self, cache: Cache, storage: Storage, tile_width: int):
        self.cache = CachedStorage(cache, storage)
        self.tile_caches = Cache(cache_folder=Path('/tmp/tiles/'))
        self.tile_width = tile_width

    def get_tile(self, image_id: str, tile_idx: int) -> typing.BinaryIO:
        cached_tile_key = f'{image_id}_{tile_idx}'
        if self.tile_caches.is_data_in_cache(cached_tile_key):
            return self.tile_caches.get_data_in_cache(cached_tile_key)
        data = self.cache.get(image_id)
        image: PIL.Image.Image = PIL.Image.open(data, formats=('PNG',))
        left_idx = self.tile_width * tile_idx
        right_idx = left_idx + self.tile_width

        cropped_image = image.crop((left_idx, 0, right_idx, image.height))
        cropped_data = io.BytesIO()
        cropped_image.save(cropped_data, format='PNG')
        cropped_data.seek(0)
        self.tile_caches.put_data_in_cache(cached_tile_key, cropped_data)
        cropped_data.seek(0)
        return cropped_data
