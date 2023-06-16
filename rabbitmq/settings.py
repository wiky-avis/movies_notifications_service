from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class RabbitMQSettings(BaseSettings):
    host: str = Field(env="RABBITMQ_HOST", default="0.0.0.0")
    port: int = Field(env="RABBITMQ_PORT", default=5672)
    username: str = Field(env="RABBITMQ_USER", default="guest")
    password: str = Field(env="RABBITMQ_PASS", default="guest")

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


settings = RabbitMQSettings()
