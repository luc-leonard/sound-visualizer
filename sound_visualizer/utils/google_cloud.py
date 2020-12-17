# this functions puts the content of the env var 'GOOGLE_CREDENTIALS'
# into the file at the env var 'GOOGLE_APPLICATION_CREDENTIALS (this env var is required by google)
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def init_google_cloud():
    credentials = os.getenv('GOOGLE_CREDENTIALS', None)
    path_to_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    logger.info(
        f'credentials present = {credentials is not None} to be put in {path_to_credentials}'
    )
    if credentials is not None and path_to_credentials is not None:
        Path(path_to_credentials).write_bytes(credentials.encode('UTF-8'))
