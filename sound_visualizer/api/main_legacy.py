import io
import logging
import threading
from uuid import uuid4

import pymongo
from flask import g, redirect, request, send_file
from werkzeug.utils import secure_filename

from sound_visualizer.api.app import app
from sound_visualizer.models.spectral_analysis_parameters import SpectralAnalysisParameters
from sound_visualizer.models.spectral_analysis_request import SpectralAnalysisFlow

logger = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def get_form():
    all_results = [
        SpectralAnalysisFlow(**data)
        for data in app.orm.find({'status': 'finished'}).sort('_id', pymongo.DESCENDING).limit(25)
    ]
    results_links = ''
    result: SpectralAnalysisFlow
    for result in all_results:
        result_url = '/result/' + result.id
        source = result.parameters
        source_url = ''
        if source.youtube_url is not None and len(source.youtube_url) > 0:
            source_url = source.youtube_url
        results_links += (
            f'<a href={source_url}> {source_url}</a> <a href={result_url}> result </a> parameters = '
            f'{result.parameters.dict(exclude={"youtube_url"})} <br />'
        )
    return f'''
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
        <br />
        <label> frame size (between 14 and 17) </label>
         2^<input type=text name=frame_size_power value=14>
        <label> overlap_factor (between 0.1 and 0.9) </label>
        <input type=text name=overlap_factor value=0.8>
         <input type=submit value=Upload>
       </form>
        <br />
        {results_links}
       <a href='https://github.com/luc-leonard/sound-visualizer/'>github</a>
       '''


def upload_file(filename, path):
    blob = g.bucket.blob(filename)
    blob.upload_from_filename(path, timeout=600)
    logger.info(f'{filename} uploaded')


@app.route('/result/<result_id>', methods=['GET'])
def get_image(result_id):
    try:
        request = app.orm.load_request_by_id(result_id)
        if request.status != 'finished':
            return request.status
        if app.cache.is_data_in_cache(result_id):
            cached_data = app.cache.get_data_in_cache(result_id)
            return send_file(cached_data, attachment_filename='_result.png', cache_timeout=0)
        else:
            logger.info('GETTING IMAGE FROM BUCKET')
            data = io.BytesIO()
            app.storage.download_to(result_id + '.png', data)
            data.seek(0)
            app.cache.put_data_in_cache(result_id, data)
            data.seek(0)
            return send_file(data, attachment_filename='_result.png', cache_timeout=0)
    except Exception as e:
        return f'Please try again later {e}'


@app.route('/', methods=['POST'])
def post_image():
    try:
        data = request.form.to_dict()

        if len(request.form['youtube_url']) == 0:
            # upload to object storage
            sound_file = request.files['sound_file']
            filename = '/tmp/' + secure_filename(sound_file.filename)
            sound_file.save(filename)
            data['filename'] = sound_file.filename

        spectral_request = SpectralAnalysisFlow(
            id='result_' + str(uuid4()),
            parameters=SpectralAnalysisParameters(**data),
            status='requested',
        )
        logger.info(spectral_request)
        app.orm.save_request(spectral_request)

        def _thread(data_cpy):
            if len(data_cpy['youtube_url']) == 0:
                upload_file(sound_file.filename, filename)
            app.publisher.publish('my-topic', spectral_request.json().encode("utf-8"))

        threading.Thread(target=_thread, args=(data,)).start()

        return redirect('/result/' + spectral_request.id)
    except Exception as e:
        return str(e), 400


# outside of main for gunicorn

if __name__ == '__main__':
    app.run()
