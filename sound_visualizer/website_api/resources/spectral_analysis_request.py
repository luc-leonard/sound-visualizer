import logging

from flask import request
from flask_restful import Resource, abort

from sound_visualizer.models.spectral_analysis_parameters import SpectralAnalysisParameters
from sound_visualizer.website_api.controller.spectral_analysis_request_handler import (
    SpectralAnalysisRequestHandler,
)

logger = logging.getLogger(__name__)


def SpectralAnalysisRequestListResource(handler: SpectralAnalysisRequestHandler):
    class SpectralAnalysisListResourceImpl(Resource):
        def __init__(self):
            self.handler = handler

        def get(self) -> list:
            offset = int(request.args.get('offset', 0))
            length = int(request.args.get('length', -1))
            status = request.args.get('status', None)

            return [o.dict() for o in self.handler.get_all_requests(offset, length, status=status)]

        def post(self) -> dict:
            logger.info(f'received request {request.json}')
            params = SpectralAnalysisParameters(**request.json)
            return self.handler.handle_new_request(params).dict()

    return SpectralAnalysisListResourceImpl


def SpectralAnalysisRequestResource(handler: SpectralAnalysisRequestHandler):
    class SpectralAnalysisResourceImpl(Resource):
        def __init__(self):
            self.handler = handler

        def get(self, analysis_id: str) -> dict:
            data = self.handler.get_request_by_id(analysis_id)
            if data is None:
                return abort(404)
            return data.dict()

    return SpectralAnalysisResourceImpl
