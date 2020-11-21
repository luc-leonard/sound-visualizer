import logging

from google.cloud import pubsub_v1

from sound_visualizer.utils.logger import init_logger

logger = logging.getLogger(__name__)
init_logger()


def callback(message):
    print(message)
    message.ack()


if __name__ == '__main__':
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path('luc-leonard-sound-visualizer', 'my-sub')
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result()
        except TimeoutError as e:
            streaming_pull_future.cancel()
            logger.warning(f'timeout due to {e}')
