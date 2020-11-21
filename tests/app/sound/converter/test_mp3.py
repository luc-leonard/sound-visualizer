import os
from pathlib import Path

import numpy as np
import pytest

from sound_visualizer.app.sound import SoundReader, SpectralAnalyzer
from sound_visualizer.app.sound.converter.mp3 import Mp3Converter


@pytest.fixture()
def datadir(request):
    filename = request.module.__file__
    test_dir = Path(os.path.dirname(filename))
    return test_dir / 'resources'


def test_should_convert_mp3(datadir):
    converted_file = Mp3Converter().convert(f'{datadir}/re_mi.mp3')
    spectral_analyzer = SpectralAnalyzer(overlap_factor=0.99, frame_size=4096)
    analysis_converted_mp3 = spectral_analyzer.get_spectrogram_data(
        SoundReader(filename=converted_file)
    )
    analysis_origin_file = spectral_analyzer.get_spectrogram_data(
        SoundReader(filename=f'{datadir}/re_mi.wav')
    )
    assert (
        analysis_converted_mp3.frequency_domain[np.argmax(analysis_converted_mp3.fft_data[0])]
        == analysis_origin_file.frequency_domain[np.argmax(analysis_origin_file.fft_data[0])]
    )
    os.unlink(converted_file)
