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

"""
Здесь указывается промежуток таймзон в который можно отправлять сообщения в очередь.
Например, если серверное время - Московское, то это GMT+3. Демон будет запускаться раз в день, в 12:00МСК.
Т.к. ночное время - это время с 23:00 до 06:00, то таймзоны установлены с GMT-3 до GMT+12 соответственно.
"""
FROM_TZ = os.getenv("FROM_TZ", default=-3)
TO_TZ = os.getenv("TO_TZ", default=12)
