import youtube_dl


class YoutubeDownloader:
    def download(self):
        with youtube_dl.YoutubeDL({'prefer_ffmpeg': True}) as ydl:
            return ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])
