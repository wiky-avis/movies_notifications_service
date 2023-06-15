from pydantic import AmqpDsn, BaseSettings, Field


class NotificationsAmqpSender(BaseSettings):
    url: AmqpDsn = Field(
        env="NOTIFICATIONS_SENDER_AMQP_URL",
        default="amqp://user:pass@127.0.0.1:8030/test",
    )
    exchange: str = Field(
        env="NOTIFICATIONS_SENDER_EXCHANGE", default="notifications"
    )
    routing_key: str = Field(
        env="NOTIFICATIONS_SENDER_ROUTING_KEY", default="delivery.created"
    )

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


notifications_amqp_settings = NotificationsAmqpSender()
