import os
import socket

from pydantic import AmqpDsn, BaseSettings, PositiveInt
from settings.base import BaseConfig
from settings.sender import NotificationsEnricherAmqpSender
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


class NotificationsEnricherConfig(BaseConfig):
    # клиенты
    auth_api_client: AuthApiSettings
    notifications_enricher_amqp_sender: NotificationsEnricherAmqpSender
    # консьюмеры
    notifications_enricher_consumer: BaseConsumerSettings


CONSUMER_TAG = (
    os.getenv("TASK_CONSUMER_TAG", default=None) or socket.gethostname()
)

NOTIFICATIONS_ENRICHER_CONSUMER = {
    "url": os.getenv(
        "NOTIFICATIONS_ENRICHER_CONSUMER_AMQP_URL",
        default="amqp://user:pass@rabbitmq:5672/test",
    ),
    "queue_name": os.getenv(
        "NOTIFICATIONS_ENRICHER_CONSUMER_QUEUE",
        default="notifications_api.created_delivery",
    ),
    "exchange_name": os.getenv(
        "NOTIFICATIONS_ENRICHER_CONSUMER_EXCHANGE",
        default="notifications_api.created_delivery",
    ),
    "routing_key": os.getenv(
        "NOTIFICATIONS_ENRICHER_CONSUMER_ROUTING_KEY",
        default="event.created",
    ),
    "consumer_tag": CONSUMER_TAG,
}
