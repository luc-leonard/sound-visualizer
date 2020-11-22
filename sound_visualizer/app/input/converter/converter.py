from abc import abstractmethod


class Converter:
    @abstractmethod
    def convert(self, filename: str, start: int = 0, length: int = -1) -> str:
        pass
