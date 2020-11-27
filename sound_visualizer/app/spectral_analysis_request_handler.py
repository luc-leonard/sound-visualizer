from typing import List
from uuid import uuid4

from sound_visualizer.app.message_queue.message_queue import MessageQueuePublisher
from sound_visualizer.app.storage.storage import Storage
from sound_visualizer.models.spectral_analysis_parameters import SpectralAnalysisParameters
from sound_visualizer.models.spectral_analysis_request import (
    SpectralAnalysisFlow,
    SpectralAnalysisFlowORM,
)


class SpectralAnalysisRequestHandler:
    def __init__(
        self,
        orm: SpectralAnalysisFlowORM,
        message_publisher: MessageQueuePublisher,
        storage: Storage,
    ):
        self.orm = orm
        self.message_publisher = message_publisher
        self.storage = storage

    def get_all_requests(self, offset: int, length: int) -> List[SpectralAnalysisFlow]:
        return self.orm.load_all_requests(offset, length)

    def get_request_by_id(self, id: str) -> SpectralAnalysisFlow:
        return self.orm.load_request_by_id(id)

    def handle_new_request(self, parameters: SpectralAnalysisParameters) -> SpectralAnalysisFlow:
        spectral_request = SpectralAnalysisFlow(
            id='result_' + str(uuid4()),
            parameters=parameters,
            status='requested',
        )
        self.message_publisher.publish('my-topic', spectral_request.json().encode("utf-8"))
        return spectral_request
