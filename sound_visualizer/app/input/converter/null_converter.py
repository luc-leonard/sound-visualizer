from sound_visualizer.app.input.converter.converter import Converter


class NullConverter(Converter):
    def convert(self, filename: str, start: int = 0, length: int = -1) -> str:
        return filename
