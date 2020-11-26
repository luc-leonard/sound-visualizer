import os

from pydantic import BaseModel


class Config(BaseModel):
    mongo_connection_string: str
    google_application_credentials: str
    google_application_project_name: str
    google_storage_bucket_name: str


def config_from_env():
    return Config(**{field: os.getenv(field.upper()) for field in Config.__fields__})
