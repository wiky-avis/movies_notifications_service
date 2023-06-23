import os
import socket

from pydantic import AmqpDsn, BaseSettings, PositiveInt
from settings.base import BaseConfig
from settings.sender import NotificationsEnricherAmqpSender
from settings.services import AuthApiSettings, TemplateApiSettings


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


class EmailConfig(BaseConfig):
    # клиенты
    template_api_client: TemplateApiSettings
    # консьюмеры
    email_consumer: BaseConsumerSettings


class ConsumersConfig(NotificationsEnricherConfig, EmailConfig):
    pass


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

EMAIL_CONSUMER = {
    "url": os.getenv(
        "EMAIL_CONSUMER_AMQP_URL",
        default="amqp://user:pass@rabbitmq:5672/test",
    ),
    "queue_name": os.getenv(
        "EMAIL_CONSUMER_QUEUE",
        default="notifications_sender.send_delivery",
    ),
    "exchange_name": os.getenv(
        "EMAIL_CONSUMER_EXCHANGE",
        default="notifications_sender.send_delivery",
    ),
    "routing_key": os.getenv(
        "EMAIL_CONSUMER_ROUTING_KEY",
        default="event.ready",
    ),
    "consumer_tag": CONSUMER_TAG,
}
