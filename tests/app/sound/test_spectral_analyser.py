import numpy as np
import pytest
from pytest_mock import MockerFixture

from sound_visualizer.app.sound import SoundReader
from sound_visualizer.app.sound.spectral_analyser import SpectralAnalyzer, get_spectogram_data
from tests.util import generate_sound


@pytest.fixture()
def sample_rate() -> int:
    return 44100


@pytest.fixture()
def frequency() -> int:
    return 1000


@pytest.mark.parametrize("frequency", range(100, 2000, 100))
def test_should_compute_fft(frequency: int):
    fft_data = get_spectogram_data(
        generate_sound(frequency=frequency, duration_second=4, sample_rate=44100),
        frame_size=2 ** 15,
        overlap_factor=0.9,
    )
    frequency_space = np.linspace(0, 44100 / 2.0, fft_data.shape[1])

    # We compare the pure sin frequency to the highest Fourier factor.
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
        SoundReader(filename='', start=0, length=-1)
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
        .get_spectrogram_data(SoundReader(filename='', start_second=0, length_second=-1))
        .high_cut(frequency + 100)
    )

    assert abs(frequency - analysis.frequency_domain[np.argmax(analysis.fft_data[0])]) <= 2
    # there should be NOTHING above frequency cut
    assert analysis.frequency_domain[-1] < frequency + 100 + 1


def test_spectral_analyser_low_cut(mocker: MockerFixture, sample_rate, frequency):
    mocker.patch(
        'scipy.io.wavfile.read',
        return_value=(
            sample_rate,
            generate_sound(frequency, duration_second=5, sample_rate=sample_rate),
        ),
    )
    analysis = (
        SpectralAnalyzer(overlap_factor=0.90, frame_size=2 ** 15)
        .get_spectrogram_data(SoundReader(filename='', start=0, length=-1))
        .low_cut(frequency - 100)
    )

    assert abs(frequency - analysis.frequency_domain[np.argmax(analysis.fft_data[0])]) <= 2
    # there should be NOTHING above frequency cut
    assert analysis.frequency_domain[0] > frequency - 100 - 1


def test_spectral_analyser_low_cut_and_high_cut(mocker: MockerFixture, sample_rate, frequency):
    mocker.patch(
        'scipy.io.wavfile.read',
        return_value=(
            sample_rate,
            generate_sound(frequency, duration_second=5, sample_rate=sample_rate),
        ),
    )
    analysis = (
        SpectralAnalyzer(overlap_factor=0.99, frame_size=2 ** 15)
        .get_spectrogram_data(SoundReader(filename='', start=0, length=-1))
        .high_cut(frequency + 100)
        .low_cut(frequency - 100)
    )

    assert abs(frequency - analysis.frequency_domain[np.argmax(analysis.fft_data[0])]) <= 2
    # there should be NOTHING above frequency cut
