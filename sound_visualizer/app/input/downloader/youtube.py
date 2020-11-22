import logging

import youtube_dl

logger = logging.getLogger(__name__)


class YoutubeHook:
    def __call__(self, *args, **kwargs):
        data = args[0]
        logger.debug(data)
        if data['status'] == 'finished':
            self.final_status = data


class YoutubeDownloader:
    def download(self, url):
        hook = YoutubeHook()
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '/tmp/%(title)s-%(id)s.%(ext)s',
            'logger': logging.getLogger(__name__),
            'progress_hooks': [hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            logger.info(f'Starting download of {url}')
            ydl.download([url])
            processed_filename = hook.final_status['filename']
            logger.info(f'{url} downloaded at {processed_filename}')
            return processed_filename
