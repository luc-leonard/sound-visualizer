import pika
import pytest

import docker
from sound_visualizer.app.message_queue.message_queue import Message
from sound_visualizer.app.message_queue.rabbitmq import RabbitMqConsumer, RabbitMqPublisher
from tests.util import docker_opts, service_hostname, try_until


@pytest.fixture(scope='module')
def rabbitmq():
    client = docker.from_env()
    rabbit_container = client.containers.run('rabbitmq:3', name='rabbit', **docker_opts(port=5672))

    def rabbit_ok():
        con = pika.BlockingConnection(
            pika.ConnectionParameters(host=service_hostname(rabbit_container.name), port=5672)
        )
        con.close()
        return True

    try_until(rabbit_ok, 100, 10000).catch(lambda ex: rabbit_container.stop()).get()

    yield rabbit_container
    rabbit_container.stop()


@pytest.fixture()
def connection(rabbitmq):
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=service_hostname(rabbitmq.name), port=5672)
    )


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
