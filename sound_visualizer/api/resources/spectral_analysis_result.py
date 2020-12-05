import logging

from flask import send_file
from flask_restful import Resource

from sound_visualizer.app.cache import Cache, CachedStorage
from sound_visualizer.app.storage.storage import Storage
from sound_visualizer.models.spectral_analysis_request import SpectralAnalysisFlowORM

logger = logging.getLogger(__name__)


def SpectralAnalysisResultResource(orm: SpectralAnalysisFlowORM, storage: Storage, cache: Cache):
    cached_storage = CachedStorage(cache, storage)

    class SpectralAnalysisResultImpl(Resource):
        def get(self, analysis_id: str):
            flow = orm.load_request_by_id(analysis_id)
            if flow.status != 'finished':
                return flow.dict()
            data = cached_storage.get(analysis_id)
            # the cache duration can be VERY high, results are immutables.
            # But since we are in a WIP, let's put it low, so we can fix things :P
            return send_file(data, attachment_filename='_result.png', cache_timeout=600)

    return SpectralAnalysisResultImpl
