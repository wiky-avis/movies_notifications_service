import os

from pydantic import AnyHttpUrl, BaseSettings


class BaseClientSettings(BaseSettings):
    url: AnyHttpUrl


class AuthApiSettings(BaseClientSettings):
    token: str


AUTH_API_SERVICE = {
    "url": os.getenv("AUTH_API_URL", default="http://0.0.0.0:8000"),
    "token": os.getenv(
        "AUTH_API_SRV_TOKEN",
        default="test",
    ),
}
