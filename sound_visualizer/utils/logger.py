import json
import logging
import sys
from typing import Dict

_LOGGING_CONF_FILE = 'logging_conf.json'


def init_logger():
    root = logging.getLogger()
    root.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)
    with open(_LOGGING_CONF_FILE) as f:
        loggers_level: Dict[str, str] = json.load(f)
        for (logger_name, logger_level) in loggers_level.items():
            logging.getLogger(logger_name).setLevel(logger_level)
