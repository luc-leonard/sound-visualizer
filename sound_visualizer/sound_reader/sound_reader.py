from typing import Tuple

import numpy as np
from pydantic import BaseModel, Field
from scipy.io import wavfile

from .fft import get_spectogram_data


class SpectralAnalyzer(BaseModel):
    frame_size: int = Field(default=2 ** 10, description="Should be a power of 2")
    overlap_factor: float = Field(ge=0.0, le=1.0)

    def get_spectrogram_data(
        self, filename: str, start: int, length: int
    ) -> Tuple[int, np.ndarray]:
        data, length = get_sound_data(filename, start, length)
        return length, get_spectogram_data(
            data, frame_size=self.frame_size, overlap_factor=self.overlap_factor
        )


def get_sound_data(filename: str, start_second: int, length_second: int) -> Tuple[np.ndarray, int]:
    sample_rate, data = wavfile.read(filename)
    # we only handle one channel

    if len(data.shape) > 1:
        data = data[:, 0]
    start_idx = start_second * sample_rate
    if length_second == -1:
        end_idx = data.shape[0] - 1
    else:
        end_idx = start_idx + (length_second * sample_rate)
    data = data[start_idx:end_idx]
    length = data.shape[0] / sample_rate
    return data, length
