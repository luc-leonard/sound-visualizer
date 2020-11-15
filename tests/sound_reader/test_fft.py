import numpy as np
import pytest

from sound_visualizer.sound_reader.fft import get_spectogram_data
from tests.sound_reader.util import generate_sound


@pytest.mark.parametrize("frequency", range(100, 2000, 100))
def test_should_compute_fft(frequency: int):
    fft_data = get_spectogram_data(
        generate_sound(frequency=frequency, duration_second=4, sample_rate=44100),
        frame_size=2 ** 15,
        overlap_factor=0.9,
    )
    frequency_space = np.linspace(0, 44100 / 2.0, fft_data.shape[1])

    assert abs(frequency - frequency_space[np.argmax(fft_data[0])]) <= 1
