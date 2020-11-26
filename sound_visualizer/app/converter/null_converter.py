from sound_visualizer.app.converter.converter import Converter


class NullConverter(Converter):
    def convert(self) -> str:
        return self.filename
