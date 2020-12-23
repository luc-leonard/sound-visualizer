import pika
import pytest

from sound_visualizer.app.message_queue.message_queue import Message
from sound_visualizer.app.message_queue.rabbitmq import RabbitMqConsumer, RabbitMqPublisher
from tests.util import service_hostname, start_container, try_until


@pytest.fixture(scope='function')
def rabbitmq():
    service = start_container(image='rabbitmq:3', service_port=5672)

    def rabbit_ok():
        con = pika.BlockingConnection(
            pika.ConnectionParameters(host=service_hostname(service.host), port=service.port)
        )
        con.close()
        return True

    try_until(rabbit_ok, 100, 10000).catch(lambda ex: service.container.stop()).get()

    yield service
    service.container.stop()


@pytest.fixture()
def connection(rabbitmq):
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=service_hostname(rabbitmq.host), port=rabbitmq.port)
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
