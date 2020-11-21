import logging

import numpy as np
from pydantic import BaseModel, Field

from sound_visualizer import utils
from sound_visualizer.app.input import SoundReader

logger = logging.getLogger(__name__)


class SpectralAnalysis(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    time_domain: np.ndarray
    frequency_domain: np.ndarray
    fft_data: np.ndarray

    def high_cut(self, cut_frequency: int) -> 'SpectralAnalysis':
        cut_idx = np.searchsorted(self.frequency_domain, cut_frequency)
        filtered_fft = self.fft_data[:, 0:cut_idx]
        new_frequency_domain = np.linspace(
            self.frequency_domain[0], cut_frequency, filtered_fft.shape[1]
        )
        return SpectralAnalysis(
            time_domain=self.time_domain,
            frequency_domain=new_frequency_domain,
            fft_data=filtered_fft,
        )

    def low_cut(self, cut_frequency: int) -> 'SpectralAnalysis':
        cut_idx = np.searchsorted(self.frequency_domain, cut_frequency)
        filtered_fft = self.fft_data[:, cut_idx : self.fft_data.shape[1] - 1]
        new_frequency_domain = np.linspace(
            cut_frequency, self.frequency_domain[-1], filtered_fft.shape[1]
        )
        return SpectralAnalysis(
            time_domain=self.time_domain,
            frequency_domain=new_frequency_domain,
            fft_data=filtered_fft,
        )


class SpectralAnalyzer(BaseModel):
    frame_size: int = Field(default=2 ** 10, description="Should be a power of 2")
    overlap_factor: float = Field(ge=0.0, le=1.0)

    def get_spectrogram_data(self, sound_reader: SoundReader) -> SpectralAnalysis:
        sound = sound_reader.get_data()
        fft_data = get_spectogram_data(
            sound.data, frame_size=self.frame_size, overlap_factor=self.overlap_factor
        )
        return SpectralAnalysis(
            time_domain=np.linspace(0, sound.length, fft_data.shape[0]),
            frequency_domain=np.linspace(0, sound.sample_rate / 2.0, fft_data.shape[1]),
            fft_data=fft_data,
        )


def get_spectogram_data(data: np.ndarray, frame_size: int, overlap_factor: float) -> np.ndarray:
    """
    :param data: the raw audio data
    :param frame_size:  the size of a frame. should be a power of 2 such as 2**12
    :param overlap_factor: how much overlap will there be between each frame ? increases quality and data size. \
    as an exemple, a ~4min track with 0.99 will take about 1Gb of memory
    :return: a 2d array. one dimension is time, the other one is frequency.
    """
    from numpy.lib import stride_tricks

    hopSize = int(frame_size - np.floor(overlap_factor * frame_size))
    samples = np.append(np.zeros(int(np.floor(frame_size / 2.0))), data)
    cols = np.ceil((len(samples) - frame_size) / float(hopSize)) + 1
    samples = np.append(samples, np.zeros(frame_size))
    # first, we create overlapping windows (in the sql sense) with as_strided.
    # then we copy them so each window will be modifiable
    frames = stride_tricks.as_strided(
        samples,
        shape=(int(cols), frame_size),
        strides=(samples.strides[0] * hopSize, samples.strides[0]),
    ).copy()
    logger.info(f'total frames size = {utils.size.convert_size(frames.nbytes)}')
    # we apply a 'window' (in the mathematical sense) function. its purpose is to make sure our lines are smooth
    frames *= np.hamming(frame_size)

    full_fft_data = 10 * np.log(10) * np.abs(np.fft.rfft(frames))
    return full_fft_data
