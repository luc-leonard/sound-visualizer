import io
import shutil

import pytest

from sound_visualizer.app.cache import Cache


@pytest.fixture()
def cache():
    shutil.rmtree('/tmp/test/', ignore_errors=True)
    return Cache(cache_folder='/tmp/test/')


@pytest.fixture()
def result_id():
    return 'FAKE_RESULT_ID'


def test_cache(cache, result_id):
    assert cache.is_data_in_cache(result_id) is False
    cache.put_data_in_cache(result_id, io.BytesIO(b'FOFOFOFO'))
    assert cache.is_data_in_cache(result_id) is True
    assert cache.get_data_in_cache(result_id).read() == b'FOFOFOFO'
