import typing
from abc import abstractmethod


class Storage:
    @abstractmethod
    def download_to(self, filname: str, to: typing.BinaryIO):
        ...

    @abstractmethod
    def upload_from(self, filename: str, _from: typing.BinaryIO):
        ...
