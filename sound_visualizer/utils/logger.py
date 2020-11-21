import logging
import sys


def init_logger():
    root = logging.getLogger()
    root.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)
