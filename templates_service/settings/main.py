from pydantic import BaseSettings, Field

from templates_service.settings.constants import (
    ADMIN_PANEL_SRV_TOKEN,
    TEST_PUBLIC_KEY,
    UGC_SRV_TOKEN,
)


class AppSettings(BaseSettings):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)


class DatabaseSettings(BaseSettings):
    url: str = Field(
        env="DATABASE_URL",
        default="postgresql://app:123qwe@notifications_db:5432/notifications",
    )
    name: str = Field(env="POSTGRES_DB", default="notifications")


class AuthSettings(BaseSettings):
    secure_key: str = Field(
        env="AUTH_SECURE_KEY", default="access_token_cookie"
    )
    jwt_algorithm: str = Field(env="JWT_ALGORITHM", default="RS256")
    jwt_secret: str = Field(env="JWT_SECRET", default=TEST_PUBLIC_KEY)
    token_header: str = Field(
        env="TOKEN_HEADER",
        default="X-AUTH-TOKEN",
    )
    tokens: set = {UGC_SRV_TOKEN, ADMIN_PANEL_SRV_TOKEN}


class AdminPanelSettings(BaseSettings):
    debug: bool = Field(env="DEBUG", default=False)
    log_format: str = Field(env="LOG_FORMAT", default="INFO")
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"
        env_nested_delimiter = "__"
        env_prefix = "TEMPLATES_"  # Templates service


settings = AdminPanelSettings()
