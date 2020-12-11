import logging
from typing import List, Optional

from _sha3 import sha3_512

from sound_visualizer.app.message_queue.message_queue import MessageQueuePublisher
from sound_visualizer.app.storage.storage import Storage
from sound_visualizer.models.spectral_analysis_parameters import SpectralAnalysisParameters
from sound_visualizer.models.spectral_analysis_request import (
    SpectralAnalysisFlow,
    SpectralAnalysisFlowORM,
)

logger = logging.getLogger(__name__)


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

    def get_request_by_id(self, id: str) -> Optional[SpectralAnalysisFlow]:
        return self.orm.load_request_by_id(id)

    def handle_new_request(self, parameters: SpectralAnalysisParameters) -> SpectralAnalysisFlow:
        id = sha3_512(
            f'{parameters.youtube_url}'
            f'_{parameters.frame_size_power}_'
            f'{parameters.overlap_factor}'.encode('utf-8')
        ).hexdigest()

        spectral_request = SpectralAnalysisFlow(
            id='result_' + id,
            parameters=parameters,
            status='requested',
        )

        maybe_existing_request = self.orm.load_request_by_id(spectral_request.id)
        if maybe_existing_request is None or maybe_existing_request.status != 'finished':
            self.orm.save_request(spectral_request)
            self.message_publisher.publish('my-topic', spectral_request.json().encode("utf-8"))
        else:
            logger.info('already computed...')
        return spectral_request
