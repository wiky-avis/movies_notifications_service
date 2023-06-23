import os

from pydantic import AnyHttpUrl, BaseSettings


class BaseClientSettings(BaseSettings):
    url: AnyHttpUrl


class AuthApiSettings(BaseClientSettings):
    token: str


class TemplateApiSettings(BaseClientSettings):
    token: str


class EmailProviderApiSettings(BaseClientSettings):
    token: str


AUTH_API_SERVICE = {
    "url": os.getenv("AUTH_API_URL", default="http://0.0.0.0:8000"),
    "token": os.getenv(
        "AUTH_API_SRV_TOKEN",
        default="test",
    ),
}

TEMPLATES_API_SERVICE = {
    "url": os.getenv("TEMPLATE_APP__URL", default="http://0.0.0.0:8002"),
    "token": os.getenv(
        "TEMPLATE_API_SRV_TOKEN",
        default="test",
    ),
}

EMAIL_PROVIDER_API_SERVICE = {
    "url": os.getenv("EMAIL_PROVIDER_API_URL", default="http://0.0.0.0:8005"),
    "token": os.getenv(
        "EMAIL_PROVIDER_TOKEN",
        default="test",
    ),
}
