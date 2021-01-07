import time
from asyncio import new_event_loop
from asyncio.futures import Future
from threading import Thread
from typing import Callable, List

import pika
from pika.adapters.blocking_connection import BlockingChannel

from sound_visualizer.app.message_queue.message_queue import (
    Message,
    MessageQueueConsumer,
    MessageQueuePublisher,
)
from sound_visualizer.config import Config


def heartbeat(connection: pika.BlockingConnection):
    while True:
        time.sleep(15)
        # it is likely that a better way exists
        try:
            connection.channel().close()
        except Exception:
            ...


def make_connection(config: Config) -> pika.BlockingConnection:
    credentials = None
    if config.rabbitmq_username is not None and config.rabbitmq_password is not None:
        credentials = pika.PlainCredentials(
            username=config.rabbitmq_username, password=config.rabbitmq_password
        )

    parameters = pika.ConnectionParameters(
        host=config.rabbitmq_hostname,
        port=config.rabbitmq_port,
        virtual_host=config.rabbitmq_vhost,
        heartbeat=15,
    )
    if credentials is not None:
        parameters.credentials = credentials
    con = pika.BlockingConnection(parameters)
    hearbeat_thread = Thread(target=heartbeat, args=[con])
    hearbeat_thread.start()
    return con


class RabbitMqPublisher(MessageQueuePublisher):
    def __init__(self, connection: pika.BlockingConnection):
        self.channel: BlockingChannel = connection.channel()

    def publish(self, routing_key: str, message) -> None:
        self.channel.basic_publish(exchange='', routing_key=routing_key, body=message)


class RabbitMqMessage(Message):
    def __init__(self, ch: BlockingChannel, method, properties, body: str):
        self.channel = ch
        self.body = body

    @property
    def data(self) -> str:
        return self.body

    def ack(self) -> None:
        ...


class RabbitMqConsumer(MessageQueueConsumer):
    def __enter__(self):
        self.event_loop.call_soon(self._start_consume)
        return self.event_loop.run_until_complete(self.future)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for tag in self.tags:
            self.channel.stop_consuming(tag)

    def __init__(self, connection: pika.BlockingConnection):
        self.channel: BlockingChannel = connection.channel()
        self.event_loop = new_event_loop()
        self.future = self.event_loop.create_future()
        self.tags: List[str] = []

    def consume(self, binding_key: str, callback: Callable[[Message], None]) -> Future:
        def _callback(ch, method, properties, body):
            callback(RabbitMqMessage(ch, method, properties, body))

        self.tags.append(
            self.channel.basic_consume(
                queue=binding_key, auto_ack=True, on_message_callback=_callback
            )
        )
        return self.future

    def close(self):
        self.future.set_result('STOP')

    def _start_consume(self):
        self.channel.start_consuming()
        self.future.set_result('')
