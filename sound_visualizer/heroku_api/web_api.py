import io
import json
import logging
import random
import threading

from flask import Flask, redirect, request, send_file
from google.cloud import pubsub_v1
from google.cloud.storage.client import Client as CloudStorageClient
from werkzeug.utils import secure_filename

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


publisher = pubsub_v1.PublisherClient()

storage_client = CloudStorageClient()
bucket = storage_client.bucket('spectrogram-images')
topic_path = publisher.topic_path('luc-leonard-sound-visualizer', 'my-topic')


def upload_file(filename, path):
    blob = bucket.blob(filename)
    blob.upload_from_filename(path, timeout=600)
    logger.info(f'{filename} uploaded')


@app.route('/result/<result_id>', methods=['GET'])
def get_image(result_id):
    logger.info('GETTING IMAGE')
    data = io.BytesIO()
    blob = bucket.blob(result_id + '.png')
    blob.download_to_file(data)
    data.seek(0)
    return send_file(data, attachment_filename='_result.png', cache_timeout=0)


@app.route('/', methods=['POST'])
def post_image():
    data = request.form.to_dict()
    data['result_id'] = 'result_' + str(random.randint(0, 100))

    if len(request.form['youtube_url']) == 0:
        # upload to object storage
        sound_file = request.files['sound_file']
        filename = '/tmp/' + secure_filename(sound_file.filename)
        sound_file.save(filename)
        data['filename'] = sound_file.filename

        def _thread(data_cpy):
            upload_file(sound_file.filename, filename)
            publisher.publish(topic_path, json.dumps(data).encode("utf-8"))

        threading.Thread(target=_thread, args=(data,)).start()
        return redirect('/result/' + data['result_id'])


if __name__ == '__main__':
    app.run()
