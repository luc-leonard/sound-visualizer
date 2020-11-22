from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel


class Converter(BaseModel):
    filename: str
    start: Optional[int] = 0
    length: Optional[int] = -1

    @abstractmethod
    def convert(self) -> str:
        pass
