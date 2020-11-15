import argparse
import logging
import math
import sys
import uuid

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sound_reader.sound_reader import SpectralAnalysis, SpectralAnalyzer
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


def save_3dplot(spectral_analysis: SpectralAnalysis, output_folder: str):
    (x, y) = np.meshgrid(
        spectral_analysis.frequency_domain,
        spectral_analysis.time_domain,
    )

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")
    ax.view_init(elev=20, azim=-45)

    the_plot = ax.plot_surface(x, y, spectral_analysis.fft_data, cmap="autumn", shade=True)
    ax.set_title("Surface Plot in Matplotlib")
    ax.set_xlabel("Frequency (hz)")
    ax.set_ylabel("Time (s)")
    ax.set_zlabel("Amplitude")

    fig.colorbar(the_plot, shrink=0.5, aspect=5)
    plt.savefig(f'{output_folder}/{uuid.uuid4()}')


def generate_heightmap(fft_data: np.ndarray):
    image_data = np.floor((fft_data / (fft_data.max() / 255))).astype('uint8')
    plt.contour(image_data)
    plt.show()
    Image.fromarray(image_data).show()


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
    parser.add_argument("--length", type=int, help="the end in the wav in second", default=-1)
    parser.add_argument(
        "--high-cut",
        type=int,
        help="the cut-off frequency. nothing above will be displayed",
        default=-1,
    )
    parser.add_argument(
        "--output-folder",
        type=str,
        help="the cut-off frequency. nothing above will be displayed",
        default='.',
    )

    return parser.parse_args()


def main():
    args = arg_parse()
    LOGGER.info(args)
    spectral_analyzer = SpectralAnalyzer(
        overlap_factor=args.overlap_factor, frame_size=args.frame_size
    )
    stopwatch = StopWatch()
    with stopwatch:
        spectral_analysis = spectral_analyzer.get_spectrogram_data(
            args.filename, args.start, args.length
        )
    LOGGER.info(f"fft transformation took {stopwatch.interval}")
    LOGGER.info(f"fft data size = {convert_size(spectral_analysis.fft_data.nbytes)}")
    LOGGER.info(f"fft data shape = {spectral_analysis.fft_data.shape}")
    if args.high_cut > 0:
        spectral_analysis = spectral_analysis.high_cut(args.high_cut)
    save_3dplot(spectral_analysis, args.output_folder)


# generate_heightmap(filtered_fft)


def init_logger():
    root = logging.getLogger()
    root.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == "__main__":
    init_logger()
    main()
