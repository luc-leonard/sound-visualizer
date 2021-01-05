import pika
import pytest

from sound_visualizer.app.message_queue.message_queue import Message
from sound_visualizer.app.message_queue.rabbitmq import RabbitMqConsumer, RabbitMqPublisher
from tests.util import start_container, try_until


@pytest.fixture(scope='function')
def rabbitmq():
    service = start_container(image='rabbitmq:3', service_port=5672)
    yield service
    service.container.stop()


@pytest.fixture()
def connection(rabbitmq):
    print(f'connecting to {rabbitmq.port}:{rabbitmq.host}')

    def connect_rabbit() -> pika.BlockingConnection:
        con = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq.host, port=rabbitmq.port)
        )
        return con

    return try_until(connect_rabbit, 100, 100000)


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
