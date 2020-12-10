import logging

from flask import send_file
from flask_restful import Resource

from sound_visualizer.app.cache import Cache, CachedStorage
from sound_visualizer.app.storage.storage import Storage

logger = logging.getLogger(__name__)


def TilesResources(storage: Storage, cache: Cache):
    cached_storage = CachedStorage(cache, storage)

    class TilesResourcesImpl(Resource):
        def get(self, result_id: str, x: int):
            logger.info(vars())
            data = cached_storage.get(f'{result_id}_{x}')
            return send_file(data, attachment_filename='_result.png', cache_timeout=10)

    return TilesResourcesImpl
