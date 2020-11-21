import io
import logging

from flask import Flask, Response, abort, request, send_file
from werkzeug.utils import secure_filename

from sound_visualizer.app.output.grey_scale_image import GreyScaleImageGenerator
from sound_visualizer.app.sound import SoundReader, SpectralAnalyzer
from sound_visualizer.app.sound.converter.mp3 import Mp3Converter
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
         <label>start (s)</label>
         <input type=text name=start_second value=0>
         <label>length (s)</label>
         <input type=text name=length_second>
         <input type=submit value=Upload>
       </form>
       <a href='https://github.com/luc-leonard/sound-visualizer/'>github</a>
       '''


converters = {'audio/mpeg': Mp3Converter().convert, 'audio/x-wav': lambda x: x}


@app.route('/', methods=['POST'])
def post_image():
    print(request.files)
    sound_file = request.files['sound_file']
    try:
        filename = secure_filename(sound_file.filename)
        sound_file.save('/tmp/' + filename)
        filename = converters[sound_file.mimetype](f'/tmp/{filename}')
        spectral_analyser = SpectralAnalyzer(frame_size=4096, overlap_factor=0.6)
        print(spectral_analyser)
        sound_reader = SoundReader(**{**request.args.to_dict(), 'filename': filename})
        spectral_analyzis = spectral_analyser.get_spectrogram_data(sound_reader)
        spectral_analyzis = spectral_analyzis.high_cut(2000)
        image_generator = GreyScaleImageGenerator(border_width=10, border_color='red')
        image = image_generator.create_image(spectral_analyzis.fft_data)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='png')
        image_bytes.seek(0)
        return send_file(image_bytes, attachment_filename='_result.png', cache_timeout=0)
    except Exception as e:
        logger.warn(e)
        abort(Response(str(e), status=500))


if __name__ == '__main__':
    app.run()
