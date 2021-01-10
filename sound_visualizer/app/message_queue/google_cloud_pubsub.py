from asyncio import Future
from typing import Callable

from google.cloud import pubsub_v1

from sound_visualizer.app.message_queue.message_queue import (
    Message,
    MessageQueueConsumer,
    MessageQueuePublisher,
)


# fake change to trigger CI. to remove ;)
class GoogleCloudPublisher(MessageQueuePublisher):
    def __init__(self, project_name: str):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_name = project_name

    def publish(self, routing_key: str, message: bytes) -> None:
        publish_path = self.publisher.topic_path(self.project_name, 'my-topic')
        self.publisher.publish(publish_path, message)


class GoogleCloudConsumer(MessageQueueConsumer):
    def __init__(self, project_name: str):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.project_name = project_name

    def consume(self, binding_key: str, callback: Callable[[Message], None]) -> Future:
        subscription_path = self.subscriber.subscription_path(self.project_name, binding_key)
        return self.subscriber.subscribe(subscription_path, callback)

    def __enter__(self):
        return self.subscriber.__enter__()

    def __exit__(self, *args):
        return self.subscriber.__exit__(*args)
