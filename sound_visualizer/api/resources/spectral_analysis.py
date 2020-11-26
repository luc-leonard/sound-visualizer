from flask_restful import Resource


class SpectralAnalysisResource(Resource):
    def get(self) -> list:
        ...
