from sound_visualizer.common.converter.converter import Converter


class NullConverter(Converter):
    def convert(self, _format: str) -> str:
        return self.filename
