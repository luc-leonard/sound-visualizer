import os
from pathlib import Path

import pytest

import sound_visualizer.api.main_docker


@pytest.fixture()
def client():
    with sound_visualizer.api.main_docker.app.test_client() as client:
        yield client


@pytest.fixture()
def datadir(request):
    filename = request.module.__file__
    test_dir = Path(os.path.dirname(filename))
    return test_dir / 'resources'


def test_should_return_ok_for_wav(client, datadir):
    data = {}
    data['sound_file'] = (open(datadir / 're_mi.wav', 'rb'), 'test.wav')
    res = client.post('/', content_type='multipart/form-data', data=data)
    assert res.status_code == 200


def test_should_return_ok_for_mp3(client, datadir):
    data = {}
    data['sound_file'] = (open(datadir / 're_mi.mp3', 'rb'), 'test.mp3')
    res = client.post('/', content_type='multipart/form-data', data=data)
    assert res.status_code == 200


def test_should_return_ok_for_youtube_url(client, datadir):
    data = {}
    data['youtube_url'] = 'https://www.youtube.com/watch?v=tkG4EMP2tC8'
    res = client.post('/', content_type='multipart/form-data', data=data)
    assert res.status_code == 200
