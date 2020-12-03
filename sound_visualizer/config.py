import os
from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    cors_origin: List[str]

    mongo_connection_string: str

    google_application_credentials: str
    google_application_project_name: str
    google_storage_bucket_name: str


def config_from_env():
    cors_origin = os.getenv('CORS_ORIGIN', '')
    splitted_cors_origin = cors_origin.split(';')
    return Config(
        cors_origin=splitted_cors_origin,
        **{
            field: os.getenv(field.upper()) for field in Config.__fields__ if field != 'cors_origin'
        },
    )
