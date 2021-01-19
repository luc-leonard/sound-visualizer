import pytest

from sound_visualizer.common.downloader import YoutubeDownloader


# This is skipped so we do not get banned from youtube :)
@pytest.mark.skip()
def test_youtube():
    downloaded_file = YoutubeDownloader().download('https://www.youtube.com/watch?v=tkG4EMP2tC8')
    assert downloaded_file is not None
