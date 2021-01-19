# import argparse
# import datetime
# import io
# import logging
# import sys
#
# import numpy as np
#
# from sound_visualizer.common.input import SoundReader
# from sound_visualizer.common.output.grey_scale_image import GreyScaleImageGenerator
# from sound_visualizer.common.sound import SpectralAnalyzer
# from sound_visualizer.utils import StopWatch, convert_size
# from sound_visualizer.utils.logger import init_logger
#
# LOGGER = logging.getLogger(__name__)
#
#
# def arg_parse():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--filename", type=str, help="the path to the wav file to analyse")
#     parser.add_argument(
#         "--frame_size",
#         type=int,
#         help="the size of each frame when computing the whole spectrogram. Should be a power of 2",
#     )
#     parser.add_argument(
#         "--overlap_factor",
#         type=float,
#         help="the overlap of the frames used to compute the spectogram",
#     )
#     parser.add_argument(
#         "--start",
#         type=int,
#         help="the start in the wav, in second",
#         default=0,
#     )
#     parser.add_argument("--length", type=int, help="the end in the wav in second", default=-1)
#     parser.add_argument(
#         "--high-cut",
#         type=int,
#         help="the higher cut-off frequency. nothing above will be displayed",
#         default=-1,
#     )
#     parser.add_argument(
#         "--low-cut",
#         type=int,
#         help="the lower cut-off frequency. nothing below will be displayed",
#         default=-1,
#     )
#     parser.add_argument(
#         "--image-folder",
#         type=str,
#         help="the cut-off frequency. nothing above will be displayed",
#         default='.',
#     )
#
#     return parser.parse_args()
#
#
# def import_file_from_stdin(path):
#     data = sys.stdin.buffer.read()
#     with open(path, mode='wb') as output_file:
#         output_file.write(data)
#
#
# def main():
#     args = arg_parse()
#     LOGGER.info(args)
#
#     spectral_analysis = compute_fft(args)
#     LOGGER.info("applying filters...")
#     if args.low_cut > 0:
#         spectral_analysis = spectral_analysis.low_cut(args.low_cut)
#     if args.high_cut > 0:
#         spectral_analysis = spectral_analysis.high_cut(args.high_cut)
#
#     LOGGER.info(f"fft data size = {convert_size(spectral_analysis.fft_data.nbytes)}")
#     LOGGER.info(f"fft data shape = {spectral_analysis.fft_data.shape}")
#     LOGGER.info(
#         f"main frequency of frame 0 {spectral_analysis.frequency_domain[np.argmax(spectral_analysis.fft_data[0])]}"
#     )
#     image_generator = GreyScaleImageGenerator(border_color='red', border_width=30)
#     image = image_generator.create_image(spectral_analysis.fft_data)
#     with io.BytesIO() as image_bytes:
#         image.save(image_bytes, format='png')
#         image_bytes.seek(0)
#         with open(
#             f'{args.output_folder}/{datetime.datetime.now().isoformat()}.png', mode='wb'
#         ) as output_file:
#             output_file.write(image_bytes.getbuffer())
#
#
# def compute_fft(args):
#     spectral_analyzer = SpectralAnalyzer(
#         overlap_factor=args.overlap_factor, frame_size=args.frame_size
#     )
#     stopwatch = StopWatch()
#     with stopwatch:
#         spectral_analysis = spectral_analyzer.get_spectrogram_data(
#             SoundReader(
#                 filename=args.filename,
#                 start_second=args.start_second,
#                 length_second=args.length_second,
#             )
#         )
#     LOGGER.info(f"fft transformation took {stopwatch.interval}")
#     LOGGER.info(f"fft data size = {convert_size(spectral_analysis.fft_data.nbytes)}")
#     LOGGER.info(f"fft data shape = {spectral_analysis.fft_data.shape}")
#     LOGGER.info(
#         f"main frequency of frame 0 {spectral_analysis.frequency_domain[np.argmax(spectral_analysis.fft_data[0])]}"
#     )
#     return spectral_analysis
#
#
# if __name__ == "__main__":
#     init_logger()
#     main()
