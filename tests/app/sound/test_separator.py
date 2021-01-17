from sound_visualizer.app.sound import SoundReader
from sound_visualizer.app.sound.separator import Separator


def test_separate():
    separator = Separator(model='spleeter:5stems')
    reader = SoundReader(
        filename='/home/lleonard/dev/perso/sound-visualizer/spleets/headroom/audio_headroom.wav'
    )
    data = separator.separate(reader.filename)
    print(data)
