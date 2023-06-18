import os

from pydantic import AmqpDsn, BaseSettings, PositiveInt
from settings.services import AuthApiSettings


class BaseConsumerSettings(BaseSettings):
    run: bool = True
    consumer_tag: str
    url: AmqpDsn
    queue_name: str
    exchange_name: str
    routing_key: str
    prefetch_count: PositiveInt = 5
    timeout: PositiveInt = 5


class BaseConfig(BaseSettings):
    class Config:
        env_nested_delimiter = "__"
        use_enum_values = True

    debug: bool = False


class NotificationsEnricherConfig(BaseConfig):
    # клиенты
    auth_api_client: AuthApiSettings
    # консьюмеры
    notifications_enricher_consumer: BaseConsumerSettings


NOTIFICATIONS_ENRICHER_CONSUMER = {
    "url": os.getenv(
        "NOTIFICATIONS_ENRICHER_CONSUMER_AMQP_URL",
        default="amqp://user:pass@127.0.0.1:8030/test",
    ),
    "queue_name": os.getenv(
        "NOTIFICATIONS_ENRICHER_CONSUMER_QUEUE",
        default="notifications.enricher",
    ),
    "exchange_name": os.getenv(
        "NOTIFICATIONS_ENRICHER_CONSUMER_EXCHANGE", default="notifications"
    ),
    "routing_key": os.getenv(
        "NOTIFICATIONS_ENRICHER_CONSUMER_ROUTING_KEY",
        default="delivery.created",
    ),
    "consumer_tag": "notifications_enricher",
}
