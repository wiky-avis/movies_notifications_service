from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class TokenSettings(BaseSettings):
    token_header: str = Field(
        env="TOKEN_HEADER",
        default="X-AUTH-TOKEN",
    )

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


token_settings = TokenSettings()
