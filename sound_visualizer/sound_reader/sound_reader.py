from typing import Tuple

import numpy as np
from pydantic import BaseModel, Field
from scipy.io import wavfile

from .fft import get_spectogram_data


class SpectralAnalysis(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    time_domain: np.ndarray
    frequency_domain: np.ndarray
    fft_data: np.ndarray

    def high_cut(self, cut_frequency: int):
        cut_idx = np.searchsorted(self.frequency_domain, cut_frequency)
        filtered_fft = self.fft_data[:, 0:cut_idx]
        new_frequency_domain = np.linspace(0, cut_frequency, filtered_fft.shape[1])
        return SpectralAnalysis(
            time_domain=self.time_domain,
            frequency_domain=new_frequency_domain,
            fft_data=filtered_fft,
        )


class SpectralAnalyzer(BaseModel):
    frame_size: int = Field(default=2 ** 10, description="Should be a power of 2")
    overlap_factor: float = Field(ge=0.0, le=1.0)

    def get_spectrogram_data(self, filename: str, start: int, length: int) -> SpectralAnalysis:
        data, sanple_rate = get_sound_data(filename, start, length)
        fft_data = get_spectogram_data(
            data, frame_size=self.frame_size, overlap_factor=self.overlap_factor
        )
        return SpectralAnalysis(
            time_domain=np.linspace(0, length, fft_data.shape[0]),
            frequency_domain=np.linspace(0, sanple_rate / 2.0, fft_data.shape[1]),
            fft_data=fft_data,
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
    return data, sample_rate
