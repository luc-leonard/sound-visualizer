import io
import logging

from flask import send_file
from flask_restful import Resource

from sound_visualizer.app.cache import Cache
from sound_visualizer.app.storage.storage import Storage

logger = logging.getLogger(__name__)


def TilesResources(storage: Storage, cache: Cache):
    class TilesResourcesImpl(Resource):
        def get(self, result_id: str, x: int):
            logger.info(vars())
            if cache.is_data_in_cache(result_id):
                data = cache.get_data_in_cache(result_id)
            else:
                logger.info('GETTING IMAGE FROM BUCKET')
                data = io.BytesIO()
                storage.download_to(result_id + '.png', data)
                data.seek(0)
                cache.put_data_in_cache(result_id, data)
                data.seek(0)
            return send_file(data, attachment_filename='_result.png', cache_timeout=10)

    return TilesResourcesImpl
