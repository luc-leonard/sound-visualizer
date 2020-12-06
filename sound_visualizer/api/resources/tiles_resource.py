import logging

from flask import send_file
from flask_restful import Resource

from sound_visualizer.app.cache import Cache
from sound_visualizer.app.storage.storage import Storage
from sound_visualizer.app.tiler import HorizontalTiler

logger = logging.getLogger(__name__)


def TilesResources(storage: Storage, cache: Cache):
    tiler = HorizontalTiler(cache, storage, 5000)

    class TilesResourcesImpl(Resource):
        def get(self, result_id: str, x: int):
            logger.info(vars())
            data = tiler.get_tile(result_id, x)
            return send_file(data, attachment_filename='_result.png', cache_timeout=10)

    return TilesResourcesImpl
