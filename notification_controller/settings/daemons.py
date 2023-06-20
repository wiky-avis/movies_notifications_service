import os

from pydantic import BaseSettings
from settings.base import BaseConfig
from settings.sender import DeliveryTriggerStarterAmqpSender


class BaseDaemonConfig(BaseSettings):
    run: bool = True
    name: str
    cron: str


class DeliveryTriggerStarterConfig(BaseConfig):
    delivery_trigger_starter_amqp_sender: DeliveryTriggerStarterAmqpSender
    delivery_trigger_starter: BaseDaemonConfig


DELIVERY_TRIGGER_STARTER = {
    "name": "delivery_trigger_starter",
    "cron": os.getenv("DELIVERY_TRIGGER_CRON", default="* * * * *"),
}
