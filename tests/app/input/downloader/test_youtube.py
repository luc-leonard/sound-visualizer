from sound_visualizer.app.input.downloader.youtube import YoutubeDownloader


def test_youtube():
    downloaded_file = YoutubeDownloader().download('https://www.youtube.com/watch?v=tkG4EMP2tC8')
    assert downloaded_file is not None
