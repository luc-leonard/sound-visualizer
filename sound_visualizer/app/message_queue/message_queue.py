from abc import abstractmethod
from asyncio import Future
from typing import Callable


class MessageQueuePublisher:
    @abstractmethod
    def publish(self, routing_key: str, message) -> None:
        ...


class Message:
    @property
    @abstractmethod
    def data(self) -> str:
        ...

    @abstractmethod
    def ack(self) -> None:
        ...


class MessageQueueConsumer:
    # the real type of callable might be implemention dependant
    @abstractmethod
    def consume(self, binding_key: str, callback: Callable[[Message], None]) -> Future:
        ...

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
