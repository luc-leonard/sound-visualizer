from spleeter.audio.adapter import get_default_audio_adapter
from spleeter.separator import Separator as SpleeterSeparator


class Separator:
    def __init__(self, model: str):
        self.separator = SpleeterSeparator(model)
        self.adapter = get_default_audio_adapter()

    def separate(self, filename: str):
        data, _ = self.adapter.load(filename, sample_rate=44100)
        return self.separator.separate(data)
