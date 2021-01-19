import pika
import pytest

from sound_visualizer.common.message_queue.message_queue import Message
from sound_visualizer.common.message_queue.rabbitmq import RabbitMqConsumer, RabbitMqPublisher
from tests.util import start_container, try_until


@pytest.fixture(scope='function')
def rabbitmq():
    service = start_container(image='rabbitmq:3', service_port=5672)
    yield service
    service.container.stop()


@pytest.fixture()
def parameters(rabbitmq) -> pika.ConnectionParameters:
    return pika.ConnectionParameters(host=rabbitmq.host, port=rabbitmq.port)


@pytest.fixture()
def connection(rabbitmq, parameters):
    print(f'connecting to {rabbitmq.port}:{rabbitmq.host}')

    def connect_rabbit() -> pika.BlockingConnection:
        con = pika.BlockingConnection(parameters)
        return con

    return try_until(connect_rabbit, 100, 100000)


def test_rabbitmq(connection, parameters):
    publisher = RabbitMqPublisher(connection, parameters)
    consumer = RabbitMqConsumer(connection)

    connection.channel().queue_declare('foobar', durable=True)
    publisher.publish('foobar', 'hello !')

    def callback(message: Message):
        assert message.data == b'hello !'
        raise BaseException()  # forces chan to close

    consumer.consume('foobar', callback)
    with consumer:
        ...
