from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel


class Converter(BaseModel):
    filename: str
    start_second: Optional[int] = 0
    length_second: Optional[int] = -1

    @abstractmethod
    def convert(self) -> str:
        pass
