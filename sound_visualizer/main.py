import argparse
import datetime
import logging
import os
import sys

import numpy as np

from sound_visualizer.output.grey_scale_image import GreyScaleImageGenerator
from sound_visualizer.sound import SoundReader, SpectralAnalyzer
from sound_visualizer.utils import StopWatch, convert_size

LOGGER = logging.getLogger(__name__)


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
    data = sys.stdin.buffer.read()
    with open(path, mode='wb') as output_file:
        output_file.write(data)


def main():
    args = arg_parse()
    LOGGER.info(args)
    if os.getenv('_IN_DOCKER'):
        import_file_from_stdin('./sound.wav')
        args.filename = 'sound.wav'

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
    image_generator = GreyScaleImageGenerator(border_color='red', border_width=30)
    image_bytes = image_generator.create_image(spectral_analysis.fft_data)

    if os.getenv('_IN_DOCKER'):
        sys.stdout.buffer.write(image_bytes.getbuffer())
    else:
        with open(
            f'{args.output_folder}/{datetime.datetime.now().isoformat()}.png', mode='wb'
        ) as output_file:
            output_file.write(image_bytes.getbuffer())


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
