from pydantic import BaseSettings, Field

from admin_panel.settings.constants import TEST_PUBLIC_KEY


class AppSettings(BaseSettings):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)


class CacheSettings(BaseSettings):
    url: str = Field(env="REDIS_URL", default="redis://redis:6379/0")
    host: str = Field(env="REDIS_HOST", default="redis")
    port: int = Field(env="REDIS_PORT", default=6379)
    db: int = Field(env="REDIS_DB", default=0)


class DatabaseSettings(BaseSettings):
    url: str = Field(
        default="postgres://app:123qwe@notifications_db:5432/notifications"
    )
    name: str = Field(env="POSTGRES_DB", default="notifications")


class AuthSettings(BaseSettings):
    secure_key: str = Field(
        env="AUTH_SECURE_KEY", default="access_token_cookie"
    )
    jwt_algorithm: str = Field(env="JWT_ALGORITHM", default="RS256")
    jwt_secret: str = Field(env="JWT_SECRET", default=TEST_PUBLIC_KEY)


class AdminPanelSettings(BaseSettings):
    debug: bool = Field(env="DEBUG", default=False)
    log_format: str = Field(env="LOG_FORMAT", default="INFO")
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()
    cache: CacheSettings = CacheSettings()
    auth: AuthSettings = AuthSettings()

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"
        env_nested_delimiter = "__"
        env_prefix = "NAP_"  # Notifications Admin Panel


settings = AdminPanelSettings()
