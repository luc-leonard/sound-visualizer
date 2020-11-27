import io
import logging

from flask import send_file
from flask_restful import Resource

from sound_visualizer.app.cache import Cache
from sound_visualizer.app.storage.storage import Storage

logger = logging.getLogger(__name__)


def SpectralAnalysisResultResource(storage: Storage, cache: Cache):
    class SpectralAnalysisResultImpl(Resource):
        def get(self, analysis_id: str):
            if cache.is_data_in_cache(analysis_id):
                data = cache.get_data_in_cache(analysis_id)
            else:
                logger.info('GETTING IMAGE FROM BUCKET')
                data = io.BytesIO()
                storage.download_to(analysis_id + '.png', data)
                data.seek(0)
                cache.put_data_in_cache(analysis_id, data)
                data.seek(0)
            # the cache duration can be VERY high, results are immutables.
            # But since we are in a WIP, let's put it low, so we can fix things :P
            return send_file(data, attachment_filename='_result.png', cache_timeout=600)

    return SpectralAnalysisResultImpl
