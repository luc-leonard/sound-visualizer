import logging

from flask import send_file
from flask_restful import Resource, abort

from sound_visualizer.common.cache import Cache, CachedStorage
from sound_visualizer.common.storage.storage import Storage

logger = logging.getLogger(__name__)


def TilesResources(storage: Storage, cache: Cache):
    cached_storage = CachedStorage(cache, storage)

    class TilesResourcesImpl(Resource):
        def get(self, result_id: str, x: int):
            try:
                data = cached_storage.get(f'{result_id}_{x}')
                return send_file(data, attachment_filename='_result.png', cache_timeout=360)
            except Exception:
                abort(404)

    return TilesResourcesImpl
