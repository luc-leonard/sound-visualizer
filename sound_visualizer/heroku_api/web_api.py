import logging
import random

from flask import Flask
from google.cloud import pubsub_v1

from sound_visualizer.app.input.converter import Mp3Converter
from sound_visualizer.utils.logger import init_logger

app = Flask(__name__)
logger = logging.getLogger(__name__)
init_logger()


@app.route('/', methods=['GET'])
def get_form():
    return '''
       <!doctype html>
       <title>Upload new File</title>
       <h1>Upload new File</h1>
       <form method=post enctype=multipart/form-data>
         <input type=file name=sound_file>
         <label>URL youtube </label>
         <input type=text name=youtube_url>
         <label>start (s)</label>
         <input type=text name=start_second value=0>
         <label>length (s)</label>
         <input type=text name=length_second>
         <input type=submit value=Upload>
       </form>
       <a href='https://github.com/luc-leonard/sound-visualizer/'>github</a>
       '''


converters = {'audio/mpeg': Mp3Converter().convert, 'audio/x-wav': lambda x: x}

publisher = pubsub_v1.PublisherClient()


@app.route('/', methods=['POST'])
def post_image():
    topic_path = publisher.topic_path('luc-leonard-sound-visualizer', 'my-topic')
    print(topic_path)
    data = "Message number {}".format(random.randint(0, 100))
    # Data must be a bytestring
    future = publisher.publish(topic_path, data.encode("utf-8"))

    return future.result()


if __name__ == '__main__':
    app.run()
