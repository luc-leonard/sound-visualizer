import logging

from flask import request
from flask_restful import Resource

from sound_visualizer.app.spectral_analysis_request_handler import SpectralAnalysisRequestHandler
from sound_visualizer.models.spectral_analysis_parameters import SpectralAnalysisParameters

logger = logging.getLogger(__name__)


def SpectralAnalysisRequestListResource(handler: SpectralAnalysisRequestHandler):
    class SpectralAnalysisListResourceImpl(Resource):
        def __init__(self):
            self.handler = handler

        def get(self) -> list:
            offset = int(request.args.get('offset', 0))
            length = int(request.args.get('length', -1))

            return [o.dict() for o in self.handler.get_all_requests(offset, length)]

        def post(self) -> dict:
            logger.info(f'received request {request.json}')
            params = SpectralAnalysisParameters(**request.json)
            self.handler.handle_new_request(params)
            return params.dict()

    return SpectralAnalysisListResourceImpl


def SpectralAnalysisRequestResource(handler: SpectralAnalysisRequestHandler):
    class SpectralAnalysisResourceImpl(Resource):
        def __init__(self):
            self.handler = handler

        def get(self, analysis_id: str) -> dict:
            return self.handler.get_request_by_id(analysis_id).dict()

    return SpectralAnalysisResourceImpl
