from sound_visualizer.app.converter.converter import Converter


class NullConverter(Converter):
    def convert(self, _format: str) -> str:
        return self.filename
