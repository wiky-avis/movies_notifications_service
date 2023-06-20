import os
import socket

from pydantic import BaseSettings
from settings.sender import DeliveryTriggerStarterAmqpSender


class BaseDaemonConfig(BaseSettings):
    run: bool = True
    name: str
    cron: str


class BaseConfig(BaseSettings):
    class Config:
        env_nested_delimiter = "__"
        use_enum_values = True

    debug: bool = False


class DeliveryTriggerStarterConfig(BaseConfig):
    delivery_trigger_starter_amqp_sender: DeliveryTriggerStarterAmqpSender
    delivery_trigger_starter: BaseDaemonConfig


DAEMON_TAG = os.getenv("DAEMON_TAG", default=None) or socket.gethostname()


DELIVERY_TRIGGER_STARTER = {
    "url": os.getenv(
        "DELIVERY_TRIGGER_STARTER_AMQP_URL",
        default="amqp://user:pass@rabbitmq:5672/test",
    ),
    "queue_name": os.getenv(
        "DELIVERY_TRIGGER_STARTER_QUEUE",
        default="notifications_api.message_sending",
    ),
    "exchange_name": os.getenv(
        "DELIVERY_TRIGGER_STARTER_EXCHANGE",
        default="notifications_api.message_sending",
    ),
    "routing_key": os.getenv(
        "DELIVERY_TRIGGER_STARTER_ROUTING_KEY",
        default="event.created",
    ),
    "daemon_tag": DAEMON_TAG,
}
