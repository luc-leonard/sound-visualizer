import os
from pathlib import Path

import numpy as np
import pytest

from sound_visualizer.app.converter.mp3 import Mp3Converter
from sound_visualizer.app.sound import SoundReader, SpectralAnalyzer


@pytest.fixture()
def datadir(request):
    filename = request.module.__file__
    test_dir = Path(os.path.dirname(filename))
    return test_dir / 'resources'


def test_should_convert_mp3(datadir):
    converted_file = Mp3Converter(filename=f'{datadir}/re_mi.mp3').convert()
    spectral_analyzer = SpectralAnalyzer(overlap_factor=0.99, frame_size=4096)
    analysis_converted_mp3 = spectral_analyzer.get_spectrogram_data(
        SoundReader(filename=converted_file)
    )
    analysis_origin_file = spectral_analyzer.get_spectrogram_data(
        SoundReader(filename=f'{datadir}/re_mi.wav')
    )
    assert (
        analysis_converted_mp3.frequency_domain[
            np.argmax(analysis_converted_mp3.fft_data.__next__()[0])
        ]
        == analysis_origin_file.frequency_domain[
            np.argmax(analysis_origin_file.fft_data.__next__()[0])
        ]
    )
    os.unlink(converted_file)


def test_mp3_converter_should_trim(datadir):
    converted_file = Mp3Converter(
        filename=f'{datadir}/re_mi.mp3', start_second=0, length_second=1
    ).convert()
    data = SoundReader(filename=converted_file).get_data()
    assert data.length > 0.9 and data.length < 1.1


def test_mp3_converter_should_trim_with_start_len(datadir):
    converted_file = Mp3Converter(
        filename=f'{datadir}/re_mi.mp3', start_second=2, length_second=-1
    ).convert()
    data = SoundReader(filename=converted_file).get_data()
    assert data.length > 0.9 and data.length < 1.1
