import logging
from typing import Optional

import numpy as np
from pydantic import BaseModel, Field

from sound_visualizer.app.input import SoundReader
from sound_visualizer.utils import convert_size
from sound_visualizer.utils.size import np_get_real_size

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

    # hop_size = 20
    hop_size = int(int(frame_size - np.floor(overlap_factor * frame_size)) / 2)
    logger.info(f'hop zise = {hop_size}')
    samples = np.append(np.zeros(int(np.floor(frame_size / 2.0))), data)
    cols = np.ceil((len(samples) - frame_size) / float(hop_size)) + 1
    samples = np.append(samples, np.zeros(frame_size))

    # first, we create overlapping windows (in the sql sense) with as_strided.
    # since those are views on the original array, it costs almost nothing in memory
    frames = stride_tricks.as_strided(
        samples,
        shape=(int(cols), frame_size),
        strides=(samples.strides[0] * hop_size, samples.strides[0]),
    )
    # todo: either make this configurable, or find an heuristic to get the optimal value
    nb_chunks = 10
    logger.info(
        f"the fft will be computed on {nb_chunks} chunks. size in memory {convert_size(np_get_real_size(frames))} "
        f"(would use {convert_size(frames.nbytes)} without strides"
    )
    # we split this array in chunks
    chunked_frames = np.array_split(frames, nb_chunks)
    window_fn = np.hamming(frame_size)

    full_fft_data: Optional[np.ndarray] = None
    for frame in chunked_frames:
        # we apply a 'window' (in the mathematical sense) function. its purpose is to make sure our lines are smooth
        # since it alter a frame, and frames are view that overlap, we need to copy data first
        local_frame = frame.copy()
        logger.info(f'chunk size: {convert_size(np_get_real_size(local_frame))}')
        local_frame *= window_fn
        frame_fft_data = 10 * np.log(10) * np.abs(np.fft.rfft(local_frame))
        if full_fft_data is not None:
            full_fft_data = np.vstack([full_fft_data, frame_fft_data])
        else:
            full_fft_data = frame_fft_data
    assert full_fft_data is not None
    logger.info(
        f' fulll fft data. shape: {full_fft_data.shape}, size: {convert_size(full_fft_data.nbytes)}'
    )
    return full_fft_data
