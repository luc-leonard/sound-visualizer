import logging
import os
from typing import Optional

import environ

logger = logging.getLogger(__name__)


@environ.config
class Config:
    @staticmethod
    def from_environ(environ) -> 'Config':
        ...

    cors_origin: str = environ.var(default='')

    mongo_connection_string: str = environ.var()

    google_credentials: Optional[str] = environ.var(default=None)
    google_application_project_name: str = environ.var()
    google_storage_bucket_name: str = environ.var()

    rabbitmq_hostname: str = environ.var(default='localhost')
    rabbitmq_port: int = environ.var(default=5672)
    rabbitmq_username: Optional[str] = environ.var(default=None)
    rabbitmq_password: Optional[str] = environ.var(default=None)


def config_from_env() -> Config:
    config = Config.from_environ(os.environ)
    return config
