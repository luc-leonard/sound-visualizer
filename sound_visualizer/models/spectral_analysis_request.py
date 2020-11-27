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


class SpectralAnalysisFlowORM:
    def __init__(self, database):
        self._collection = database[_COLLECTION_NAME]

    def save_request(self, analysis: SpectralAnalysisFlow):
        self._collection.insert_one(analysis.dict())

    def update_request_status(self, request_id, new_status):
        self._collection.update_one({'id': request_id}, {'$set': {'status': new_status}})

    def add_stopwatch(self, request_id, stopwatch_name, time_spent):
        self._collection.update_one(
            {'id': request_id}, {'$set': {f'stopwatches.{stopwatch_name}': time_spent}}
        )

    def add_memory_used(self, request_id, name, value):
        self._collection.update_one({'id': request_id}, {'$set': {f'memory_used.{name}': value}})

    def load_request_by_id(self, request_id) -> SpectralAnalysisFlow:
        return SpectralAnalysisFlow(**self._collection.find_one({'id': request_id}))

    def load_all_requests(self, offset: int = 0, len: int = -1) -> List[SpectralAnalysisFlow]:
        if len == -1:
            requests = self._collection.find()[offset:]
        else:
            requests = self._collection.find()[offset:len]
        return [SpectralAnalysisFlow(**data) for data in requests]

    def find(self, *args, **kwargs):
        return self._collection.find(*args, **kwargs)
