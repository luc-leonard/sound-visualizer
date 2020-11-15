import argparse
import logging
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from sound_reader.sound_reader import SpectralAnalyzer
from utils.stopwatch import StopWatch

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
    frequency_cut_top = 100
    filtered_fft = fft_data[:, 0 : int(frequency_cut_top / 10)]

    (x, y) = np.meshgrid(
        np.linspace(0, frequency_cut_top, filtered_fft.shape[1]),
        np.linspace(0, length, filtered_fft.shape[0]),
    )

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")
    ax.view_init(elev=20, azim=-45)

    the_plot = ax.plot_surface(x, y, filtered_fft, cmap="autumn", shade=True)
    ax.set_title("Surface Plot in Matplotlib")
    ax.set_xlabel("Frequency (hz)")
    ax.set_ylabel("Time (s)")
    ax.set_zlabel("Amplitude")

    fig.colorbar(the_plot, shrink=0.5, aspect=5)
    plt.show()


def generate_heightmap(fft_data: np.ndarray):
    image_data = np.floor((fft_data / (fft_data.max() / 255))).astype(int)
    plt.contour(image_data)
    plt.show()


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="the path to the wav file to analyse")
    parser.add_argument(
        "--frame_size",
        type=int,
        help="the size of each frame when computing the whole spectrogram. Should be a power of 2",
    )
    parser.add_argument(
        "--overlap_factor",
        type=float,
        help="the overlap of the frames used to compute the spectogram",
    )
    parser.add_argument(
        "--start",
        type=int,
        help="the start in the wav, in second",
        default=0,
    )
    parser.add_argument("--end", type=int, help="the end in the wav in second", default=-1)
    return parser.parse_args()


def main():
    args = arg_parse()
    LOGGER.info(args)
    sound_reader = SpectralAnalyzer(overlap_factor=args.overlap_factor, frame_size=args.frame_size)
    stopwatch = StopWatch()
    with stopwatch:
        length, fft_data = sound_reader.get_spectrogram_data(args.filename, args.start, args.end)
    LOGGER.info(f"fft transformation took {stopwatch.interval}")
    LOGGER.info(f"fft data size = {convert_size(fft_data.nbytes)}")
    display_3dplot(fft_data, length)
    generate_heightmap(fft_data)


def init_logger():
    root = logging.getLogger()
    root.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == "__main__":
    import os

    print(os.getcwd())
    print(os.listdir())
    init_logger()
    main()
