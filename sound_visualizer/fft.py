import numpy as np
from numpy.lib import stride_tricks


def get_spectogram_data(data: np.ndarray, frame_size: int, overlap_factor: float) -> np.ndarray:
    """
    :param data: the raw audio data
    :param frame_size:  the size of a frame. should be a power of 2 such as 2**12
    :param overlap_factor: how much overlap will there be between each frame ? increases quality and data size. \
    as an exemple, a ~4min track with 0.99 will take about 1Gb of memory
    :return: a 2d array. one dimension is time, the other one is frequency.
    """
    hopSize = int(frame_size - np.floor(overlap_factor * frame_size))
    samples = np.append(np.zeros(int(np.floor(frame_size / 2.0))), data)
    cols = np.ceil((len(samples) - frame_size) / float(hopSize)) + 1
    samples = np.append(samples, np.zeros(frame_size))
    frames = stride_tricks.as_strided(samples, shape=(int(cols), frame_size),
                                      strides=(samples.strides[0] * hopSize, samples.strides[0])).copy()
    frames *= np.hamming(frame_size)
    full_fft_data = 10 * np.log(10) * np.abs(np.fft.rfft(frames))
    return full_fft_data