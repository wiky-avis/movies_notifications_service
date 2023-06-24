from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8003)


class DatabaseSettings(BaseSettings):
    url: str = Field(
        env="DATABASE_URL",
        default="postgresql://login:password@db:5432/notifications",
    )
    name: str = Field(env="POSTGRES_DB", default="notifications")


class TokenSettings(BaseSettings):
    header: str = Field(
        env="TOKEN_HEADER",
        default="X-AUTH-TOKEN",
    )
    token: str = Field(env="NOTIFICATIONS_ADMIN_SRV_TOKEN", default="test")


class TemplatesSettings(BaseSettings):
    host: str = Field(env="TEMPLATE_APP__HOST", default="0.0.0.0")
    port: int = Field(env="TEMPLATE_APP__PORT", default=8002)
    url: str = Field(env="TEMPLATE_APP__URL", default="https://0.0.0.0:8002")


class DeliveriesSettings(BaseSettings):
    host: str = Field(env="NA_APP_HOST", default="0.0.0.0")
    port: int = Field(env="NA_APP_PORT", default=8001)
    url: str = Field(env="TEMPLATE_APP__URL", default="https://0.0.0.0:8001")


class AdminPanelSettings(BaseSettings):
    debug: bool = Field(env="DEBUG", default=False)
    log_format: str = Field(env="LOG_FORMAT", default="INFO")
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()
    token: TokenSettings = TokenSettings()
    templates: TemplatesSettings = TemplatesSettings()
    deliveries: DeliveriesSettings = DeliveriesSettings()

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"
        env_nested_delimiter = "__"
        env_prefix = "NAP_"  # Notifications Admin Panel


settings = AdminPanelSettings()
