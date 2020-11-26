from flask_restful import Resource

from sound_visualizer.models.spectral_analysis_request import SpectralAnalysisRequestORM


def SpectralAnalysisResource(orm: SpectralAnalysisRequestORM):
    class InnerClass(Resource):
        def __init__(self):
            self.orm = orm

        def get(self) -> list:
            return [o.dict() for o in self.orm.load_all_requests()]

    return InnerClass
