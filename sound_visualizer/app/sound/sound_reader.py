import logging

import numpy as np
from pydantic import BaseModel
from scipy.io import wavfile

logger = logging.getLogger(__name__)


class Sound(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    data: np.ndarray
    sample_rate: int

    @property
    def length(self):
        return self.data.shape[0] / self.sample_rate


class SoundReader(BaseModel):
    filename: str
    start_second: int = 0
    length_second: int = -1

    def get_data(self) -> Sound:
        sample_rate, data = wavfile.read(self.filename)
        logger.info(f'{self.filename} read in memory. sample_rate = {sample_rate}')

        # if len(data.shape) > 1:
        #     data = data[:, 0]
        start_idx = self.start_second * sample_rate
        if self.length_second == -1:
            end_idx = data.shape[0] - 1
        else:
            end_idx = start_idx + (self.length_second * sample_rate)
        data = data[start_idx:end_idx]
        return Sound(data=data, sample_rate=sample_rate)
