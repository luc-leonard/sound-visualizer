# this functions puts the content of the env var 'GOOGLE_CREDENTIALS'
# into the file at the env var 'GOOGLE_APPLICATION_CREDENTIALS (this env var is required by google)
import logging
import os
from pathlib import Path

from sound_visualizer.config import Config

logger = logging.getLogger(__name__)


def init_google_cloud(config: Config):
    path_to_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    logger.info(
        f'credentials present = {config.google_credentials is not None} to be put in {path_to_credentials}'
    )
    if config.google_credentials is not None and path_to_credentials is not None:
        Path(path_to_credentials).write_bytes(config.google_credentials.encode('UTF-8'))
