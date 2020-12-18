import random

import pika
import pytest

import docker
from sound_visualizer.app.message_queue.message_queue import Message
from sound_visualizer.app.message_queue.rabbitmq import RabbitMqConsumer, RabbitMqPublisher
from tests.util import try_until


@pytest.fixture(scope='module')
def port() -> int:
    return random.randint(1500, 4500)


@pytest.fixture(scope='module')
def rabbitmq(port):
    client = docker.from_env()
    rabbit_container = client.containers.run('rabbitmq:3', ports={5672: port}, detach=True)

    def rabbit_ok():
        con = pika.BlockingConnection(pika.ConnectionParameters(port=port))
        con.close()
        return True

    try_until(rabbit_ok, 100, 10000).get()
    yield rabbit_container
    rabbit_container.stop()


@pytest.fixture()
def connection(rabbitmq, port):
    return pika.BlockingConnection(pika.ConnectionParameters(port=port))


def test_rabbitmq(connection):
    publisher = RabbitMqPublisher(connection)
    consumer = RabbitMqConsumer(connection)

    connection.channel().queue_declare('foobar')
    publisher.publish('foobar', 'hello !')

    def callback(message: Message):
        consumer.close()
        assert message.data == 'hello!'

    consumer.consume('foobar', callback)
    with consumer:
        ...
