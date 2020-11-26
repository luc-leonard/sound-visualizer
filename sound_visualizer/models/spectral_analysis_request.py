from typing import Dict, List

from pydantic import BaseModel

from sound_visualizer.models.spectral_analysis_parameters import SpectralAnalysisParameters

_COLLECTION_NAME = 'spectral-analysis'


class SpectralAnalysisFlow(BaseModel):
    id: str
    parameters: SpectralAnalysisParameters
    # how much time each step took ?
    stopwatches: Dict[str, float] = {}
    # how much memory consumed by numpy ?
    memory_used: Dict[str, int] = {}
    # really an enum but pymongo complains :(
    status: str


class SpectralAnalysisRequestORM:
    def __init__(self, database):
        self._collection = database[_COLLECTION_NAME]

    def save_request(self, analysis: SpectralAnalysisFlow):
        self._collection.insert_one(analysis.dict())

    def update_request_status(self, request_id, new_status):
        self._collection.update_one({'id': request_id}, {'$set': {'status': new_status}})

    def load_request_by_id(self, request_id) -> SpectralAnalysisFlow:
        return SpectralAnalysisFlow(**self._collection.find_one({'id': request_id}))

    def load_all_requests(self) -> List[SpectralAnalysisFlow]:
        return [SpectralAnalysisFlow(**data) for data in self._collection.find()]
