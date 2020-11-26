from abc import abstractmethod
from asyncio import Future
from typing import Callable


class MessageQueuePublisher:
    @abstractmethod
    def publish(self, routing_key: str, message) -> Future:
        ...


class MessageQueueConsumer:
    # the real type of callable might be implemention dependant
    @abstractmethod
    def consume(self, binding_key: str, callback: Callable) -> Future:
        ...

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self):
        ...
