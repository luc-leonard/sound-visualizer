import io
import json
import logging
import threading
from uuid import uuid4

from flask import g, redirect, request, send_file
from werkzeug.utils import secure_filename

from sound_visualizer.heroku_api.web.app import MyApp
from sound_visualizer.utils.logger import init_logger

app = MyApp(__name__)

logger = logging.getLogger(__name__)


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
         <input type=text name=start_second value='0'>
         <label>length (s)</label>
         <input type=text name=length_second value='-1'>
         <input type=submit value=Upload>
       </form>
       <a href='https://github.com/luc-leonard/sound-visualizer/'>github</a>
       '''


def upload_file(filename, path):
    blob = g.bucket.blob(filename)
    blob.upload_from_filename(path, timeout=600)
    logger.info(f'{filename} uploaded')


@app.route('/result/<result_id>', methods=['GET'])
def get_image(result_id):
    try:
        logger.info('GETTING IMAGE')
        data = io.BytesIO()
        blob = app.bucket.blob(result_id + '.png')
        blob.download_to_file(data)
        data.seek(0)
        return send_file(data, attachment_filename='_result.png', cache_timeout=0)
    except Exception as e:
        return f'Please try again later {e}'


@app.route('/', methods=['POST'])
def post_image():
    logger.info(app.publisher)
    data = request.form.to_dict()
    data['result_id'] = 'result_' + str(uuid4())

    if len(request.form['youtube_url']) == 0:
        # upload to object storage
        sound_file = request.files['sound_file']
        filename = '/tmp/' + secure_filename(sound_file.filename)
        sound_file.save(filename)
        data['filename'] = sound_file.filename

    def _thread(data_cpy):
        if len(data_cpy['youtube_url']) == 0:
            upload_file(sound_file.filename, filename)
        app.publisher.publish(app.topic_path, json.dumps(data_cpy).encode("utf-8"))

    threading.Thread(target=_thread, args=(data,)).start()
    return redirect('/result/' + data['result_id'])


if __name__ == '__main__':
    init_logger()
    app.run()
