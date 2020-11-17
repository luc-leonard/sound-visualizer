import argparse
import datetime
import logging
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from sound import SoundReader, SpectralAnalysis, SpectralAnalyzer
from utils import StopWatch, convert_size

LOGGER = logging.getLogger(__name__)


def save_3dplot(spectral_analysis: SpectralAnalysis, output_folder: str):
    (x, y) = np.meshgrid(
        spectral_analysis.frequency_domain,
        spectral_analysis.time_domain,
    )

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")
    ax.view_init(elev=20, azim=45)

    the_plot = ax.plot_surface(x, y, spectral_analysis.fft_data, cmap="autumn", shade=True)
    ax.set_title("Surface Plot in Matplotlib")
    ax.set_xlabel("Frequency (hz)")
    ax.set_ylabel("Time (s)")
    ax.set_zlabel("Amplitude")

    fig.colorbar(the_plot, shrink=0.5, aspect=5)
    filename = f'{output_folder}/{datetime.datetime.now().isoformat()}.png'
    plt.savefig(filename)
    return filename


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
        help="the higher cut-off frequency. nothing above will be displayed",
        default=-1,
    )
    parser.add_argument(
        "--low-cut",
        type=int,
        help="the lower cut-off frequency. nothing below will be displayed",
        default=-1,
    )
    parser.add_argument(
        "--output-folder",
        type=str,
        help="the cut-off frequency. nothing above will be displayed",
        default='.',
    )
    return parser.parse_args()


def import_file_from_stdin(path):
    output_file = open(path, mode='wb')
    data = sys.stdin.buffer.read()
    output_file.write(data)


def main():
    args = arg_parse()
    LOGGER.info(args)
    if os.getenv('_IN_DOCKER'):
        import_file_from_stdin('./sound.wav')
        args.filename = './sound.wav'
    spectral_analysis = compute_fft(args)
    LOGGER.info("applying filters...")
    if args.low_cut > 0:
        spectral_analysis = spectral_analysis.low_cut(args.low_cut)
    if args.high_cut > 0:
        spectral_analysis = spectral_analysis.high_cut(args.high_cut)

    LOGGER.info(f"fft data size = {convert_size(spectral_analysis.fft_data.nbytes)}")
    LOGGER.info(f"fft data shape = {spectral_analysis.fft_data.shape}")
    LOGGER.info(
        f"main frequency of frame 0 {spectral_analysis.frequency_domain[np.argmax(spectral_analysis.fft_data[0])]}"
    )
    saved_file = save_3dplot(spectral_analysis, args.output_folder)
    if os.getenv('_IN_DOCKER'):
        with open(saved_file, 'rb') as fin:
            sys.stdout.buffer.write(fin.read())


def compute_fft(args):
    spectral_analyzer = SpectralAnalyzer(
        overlap_factor=args.overlap_factor, frame_size=args.frame_size
    )
    stopwatch = StopWatch()
    with stopwatch:
        spectral_analysis = spectral_analyzer.get_spectrogram_data(
            SoundReader(filename=args.filename, start_second=args.start, length_second=args.length)
        )
    LOGGER.info(f"fft transformation took {stopwatch.interval}")
    LOGGER.info(f"fft data size = {convert_size(spectral_analysis.fft_data.nbytes)}")
    LOGGER.info(f"fft data shape = {spectral_analysis.fft_data.shape}")
    LOGGER.info(
        f"main frequency of frame 0 {spectral_analysis.frequency_domain[np.argmax(spectral_analysis.fft_data[0])]}"
    )
    return spectral_analysis


def init_logger():
    root = logging.getLogger()
    root.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == "__main__":
    init_logger()
    main()
