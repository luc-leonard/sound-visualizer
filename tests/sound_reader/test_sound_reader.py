import pytest
from pytest_mock import MockerFixture

from sound_visualizer.sound_reader.sound_reader import get_sound_data
from tests.sound_reader.util import generate_sound


@pytest.fixture()
def sample_rate() -> int:
    return 44100


@pytest.fixture()
def frequency() -> int:
    return 1500


@pytest.fixture()
def fake_sound(sample_rate):
    return generate_sound(frequency=200, duration_second=10, sample_rate=sample_rate)


def test_get_sound_data(mocker: MockerFixture, fake_sound, sample_rate):
    mocker.patch('scipy.io.wavfile.read', return_value=(sample_rate, fake_sound))
    data, len = get_sound_data('foo_bar', start_second=0, length_second=-1)
    # check that the signal is about 10s in len
    assert abs(10 - len) <= 0.1


def test_get_sound_data_with_len(mocker: MockerFixture, fake_sound, sample_rate):
    mocker.patch('scipy.io.wavfile.read', return_value=(sample_rate, fake_sound))
    data, len = get_sound_data('foo_bar', start_second=0, length_second=1)
    # check that the signal is about 10s in len
    assert abs(1 - len) <= 0.1
    assert (data == fake_sound[0:sample_rate]).all()


def test_get_sound_data_with_start(mocker: MockerFixture, fake_sound, sample_rate):
    mocker.patch('scipy.io.wavfile.read', return_value=(sample_rate, fake_sound))
    data, len = get_sound_data('foo_bar', start_second=7, length_second=-1)
    # check that the signal is about 10s in len
    assert abs(3 - len) <= 0.1
    assert (data == fake_sound[7 * sample_rate : fake_sound.shape[0] - 1]).all()
