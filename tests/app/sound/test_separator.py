import pytest

from sound_visualizer.common.sound import SoundReader
from sound_visualizer.common.sound.separator import Separator


@pytest.mark.skip()
def test_separate():
    separator = Separator(model='spleeter:5stems')
    reader = SoundReader(
        filename='/home/lleonard/dev/perso/sound-visualizer/spleets/headroom/audio_headroom.wav'
    )
    data = separator.separate(reader.filename)
    print(data)
