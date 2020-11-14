import sys

import numpy as np
from scipy.io import wavfile
from numpy.lib import stride_tricks
import math
import logging
import matplotlib.pyplot as plt
from PIL import Image
import scipy.misc as mi

from sound_visualizer.fft import get_spectogram_data

LOGGER = logging.getLogger(__name__)


def convert_size(size_bytes):

    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def display_3dplot(fft_data, length):
    frequency_cut_top = 1000
    filtered_fft = fft_data[:, 0:int(frequency_cut_top / 10)]

    (x, y) = np.meshgrid(np.linspace(0, frequency_cut_top, filtered_fft.shape[1]),
                         np.linspace(0, length, filtered_fft.shape[0]))

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=20, azim=75)

    the_plot = ax.plot_surface(x, y, filtered_fft, cmap='autumn', shade=True)
    ax.set_title('Surface Plot in Matplotlib')
    ax.set_xlabel('Frequency (hz)')
    ax.set_ylabel('Time (s)')
    ax.set_zlabel('Amplitude')

    fig.colorbar(the_plot, shrink=0.5, aspect=5)
    plt.show()


def main():

    sample_rate, data = wavfile.read('../sounds/Noisia & The Upbeats - Dustup-JnhjWUepaE8.wav')
    length = data.shape[0] / sample_rate
    if len(data.shape) > 1:
        data = data[:, 0]
    fft_data = get_spectogram_data(data, 2**10, 0.90)
    LOGGER.info(f'fft data size = {convert_size(fft_data.nbytes)}')
    display_3dplot(fft_data, length)


if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    import timeit

    print(timeit.timeit('main()', globals=globals(), number=1))
    main()
