from flask import Flask, request, send_file
from werkzeug.utils import secure_filename

from sound_visualizer.app.output.grey_scale_image import GreyScaleImageGenerator
from sound_visualizer.app.sound import SoundReader, SpectralAnalyzer

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_form():
    return '''
       <!doctype html>
       <title>Upload new File</title>
       <h1>Upload new File</h1>
       <form method=post enctype=multipart/form-data>
         <input type=file name=wav_file>
         <label>start (s)</label>
         <input type=text name=start_second value=0>
         <label>length (s)</label>
         <input type=text name=length_second>
         <input type=submit value=Upload>
       </form>
       '''


@app.route('/', methods=['POST'])
def post_image():
    print(request.files)
    wav_file = request.files['wav_file']
    filename = secure_filename(wav_file.filename)
    wav_file.save('/tmp/' + filename)
    spectral_analyser = SpectralAnalyzer(frame_size=4096, overlap_factor=0.6)
    print(spectral_analyser)
    sound_reader = SoundReader(**{**request.args.to_dict(), 'filename': '/tmp/' + filename})
    spectral_analyzis = spectral_analyser.get_spectrogram_data(sound_reader)
    spectral_analyzis = spectral_analyzis.high_cut(2000)
    image_generator = GreyScaleImageGenerator(border_width=10, border_color='red')
    image = image_generator.create_image(spectral_analyzis.fft_data)
    return send_file(image, attachment_filename='_result.png', cache_timeout=0)


if __name__ == '__main__':
    app.run()
