from typing import Dict, List, Optional

import pymongo
from pydantic import BaseModel

from sound_visualizer.models.spectral_analysis_parameters import SpectralAnalysisParameters

_COLLECTION_NAME = 'spectral-analysis'


class SpectralAnalysisResult(BaseModel):
    width: Optional[int]
    tile_width: Optional[int]
    height: Optional[int]


class SpectralAnalysisFlow(BaseModel):
    id: str
    title: Optional[str]
    duration: Optional[float]
    parameters: SpectralAnalysisParameters
    # how much time each step took ?
    stopwatches: Dict[str, float] = {}
    # how much memory consumed by numpy ?
    memory_used: Dict[str, int] = {}
    # really an enum but pymongo complains :(
    status: str
    result: Optional[SpectralAnalysisResult]


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

    def save_duration(self, request_id, duration):
        self._collection.update_one({'id': request_id}, {'$set': {'duration': duration}})

    def add_memory_used(self, request_id, name, value):
        self._collection.update_one({'id': request_id}, {'$set': {f'memory_used.{name}': value}})

    def load_request_by_id(self, request_id) -> Optional[SpectralAnalysisFlow]:
        data = self._collection.find_one({'id': request_id})
        if data is None:
            return None
        return SpectralAnalysisFlow(**data)

    def load_all_requests(self, offset: int = 0, len: int = -1) -> List[SpectralAnalysisFlow]:
        cursor = self._collection.find().sort('_id', pymongo.DESCENDING)

        if len == -1:
            requests = cursor[offset:]
        else:
            requests = cursor[offset:len]
        return [SpectralAnalysisFlow(**data) for data in requests]

    def find(self, *args, **kwargs):
        return self._collection.find(*args, **kwargs)

    def save_tile_size(self, id, size):
        self._collection.update_one({'id': id, 'result': None}, {'$set': {'result': {}}})
        self._collection.update_one({'id': id}, {'$set': {'result.tile_width': size}})

    def save_title(self, id, title):
        self._collection.update_one({'id': id}, {'$set': {'title': title}})

    def save_image_size(self, id, size):
        self._collection.update_one({'id': id, 'result': None}, {'$set': {'result': {}}})
        self._collection.update_one(
            {'id': id}, {'$set': {'result.width': size[0], 'result.height': size[1]}}
        )
