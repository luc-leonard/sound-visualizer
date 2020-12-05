import io
import logging
import typing

from sound_visualizer.app.cache import Cache
from sound_visualizer.app.storage.storage import Storage

logger = logging.getLogger(__name__)


class HorizontalTiler:
    def __init__(self, cache: Cache, storage: Storage):
        self.cache = cache
        self.storage = storage

    def get_tile(self, image_id: str, tile_idx: int) -> typing.BinaryIO:
        self._load_image_if_necessary(image_id)
        return io.BytesIO()

    def _load_image_if_necessary(self, image_id) -> None:
        logger.info(vars())
        if self.cache.is_data_in_cache(image_id):
            data = self.cache.get_data_in_cache(image_id)
        else:
            logger.info('GETTING IMAGE FROM BUCKET')
            data = io.BytesIO()
            self.storage.download_to(image_id + '.png', data)
            data.seek(0)
            self.cache.put_data_in_cache(image_id, data)
            data.seek(0)
