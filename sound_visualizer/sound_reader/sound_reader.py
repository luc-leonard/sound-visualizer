import numpy as np
from pydantic import BaseModel, Field
from scipy.io import wavfile

from .fft import get_spectogram_data


class SoundReader(BaseModel):
    frame_size: int = Field(default=2 ** 10, description='Should be a power of 2')
    overlap_factor: float = Field(ge=0.0, le=1.0)

    def get_spectrogram_data(self, filename: str, start: int = 0, length: int = -1) -> (int, np.ndarray):
        data, length = get_sound_data(filename, start, length)
        return length, get_spectogram_data(data, frame_size=self.frame_size, overlap_factor=self.overlap_factor)


def get_sound_data(filename: str, start: int = 0, length: int = -1) -> (np.ndarray, int):
    sample_rate, data = wavfile.read(filename)
    # we only handle one channel
    if len(data.shape) > 1:
        data = data[:, 0]
    if length == -1:
        end = data.shape[0] - start
    else:
        end = start + length
    data = data[start:end]
    length = data.shape[0] / sample_rate
    return data, length
