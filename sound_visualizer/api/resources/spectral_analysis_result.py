import logging

from flask_restful import Resource, abort

from sound_visualizer.app.cache import Cache
from sound_visualizer.app.storage.storage import Storage
from sound_visualizer.models.spectral_analysis_request import SpectralAnalysisFlowORM

logger = logging.getLogger(__name__)


def SpectralAnalysisResultResource(orm: SpectralAnalysisFlowORM, storage: Storage, cache: Cache):
    class SpectralAnalysisResultImpl(Resource):
        def get(self, analysis_id: str):
            flow = orm.load_request_by_id(analysis_id)
            if flow is None:
                return abort(404)
            return flow.dict()

    return SpectralAnalysisResultImpl
