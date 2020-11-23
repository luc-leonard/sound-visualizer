import os

from pydantic import BaseModel


class Config(BaseModel):
    mongo_username: str
    mongo_password: str


def config_from_env():
    return Config(**{field: os.getenv(field.upper()) for field in Config.__fields__})
