import logging

import youtube_dl


class YoutubeHook:
    def __call__(self, *args, **kwargs):
        data = args[0]
        if data['status'] == 'finished':
            self.final_status = data


class YoutubeDownloader:
    def download(self, url):
        hook = YoutubeHook()
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '/tmp/%(title)s-%(id)s.%(ext)s',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
            'logger': logging.getLogger(__name__),
            'progress_hooks': [hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return hook.final_status['filename'][0:-4] + '.mp3'
