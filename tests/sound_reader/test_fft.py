import numpy as np
import pytest
from pytest_mock import MockerFixture
from sound_reader.sound_reader import SpectralAnalyzer

from sound_visualizer.sound_reader.fft import get_spectogram_data
from tests.sound_reader.util import generate_sound


@pytest.fixture()
def sample_rate() -> int:
    return 44100


@pytest.fixture()
def frequency() -> int:
    return 200


@pytest.mark.parametrize("frequency", range(100, 2000, 100))
def test_should_compute_fft(frequency: int):
    fft_data = get_spectogram_data(
        generate_sound(frequency=frequency, duration_second=4, sample_rate=44100),
        frame_size=2 ** 15,
        overlap_factor=0.9,
    )
    frequency_space = np.linspace(0, 44100 / 2.0, fft_data.shape[1])

    assert abs(frequency - frequency_space[np.argmax(fft_data[0])]) <= 1


def test_spectral_analyser(mocker: MockerFixture, sample_rate, frequency):
    mocker.patch(
        'scipy.io.wavfile.read',
        return_value=(
            sample_rate,
            generate_sound(frequency, duration_second=5, sample_rate=sample_rate),
        ),
    )
    analysis = SpectralAnalyzer(overlap_factor=0.90, frame_size=2 ** 15).get_spectrogram_data(
        '', start=0, length=-1
    )

    assert abs(frequency - analysis.frequency_domain[np.argmax(analysis.fft_data[0])]) <= 1


def test_spectral_analyser_high_cut(mocker: MockerFixture, sample_rate, frequency):
    mocker.patch(
        'scipy.io.wavfile.read',
        return_value=(
            sample_rate,
            generate_sound(frequency, duration_second=5, sample_rate=sample_rate),
        ),
    )
    analysis = (
        SpectralAnalyzer(overlap_factor=0.90, frame_size=2 ** 15)
        .get_spectrogram_data('', start=0, length=-1)
        .high_cut(frequency + 50)
    )

    assert abs(frequency - analysis.frequency_domain[np.argmax(analysis.fft_data[0])]) <= 2
