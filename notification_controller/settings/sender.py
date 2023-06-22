import os

from pydantic import AmqpDsn, BaseSettings


class BaseSenderSettings(BaseSettings):
    run: bool = True
    url: AmqpDsn
    exchange: str


class NotificationsEnricherAmqpSender(BaseSenderSettings):
    pass


class DeliveryTriggerStarterAmqpSender(BaseSenderSettings):
    pass


NOTIFICATIONS_ENRICHER_SENDER = {
    "url": os.getenv(
        "NOTIFICATIONS_ENRICHER_SENDER_AMQP_URL",
        default="amqp://user:pass@rabbitmq:5672/test",
    ),
    "exchange": os.getenv(
        "NOTIFICATIONS_ENRICHER_SENDER_EXCHANGE",
        default="notifications_sender.send_delivery",
    ),
}

DELIVERY_TRIGGER_STARTER_SENDER = {
    "url": os.getenv(
        "DELIVERY_TRIGGER_STARTER_SENDER_AMQP_URL",
        default="amqp://user:pass@rabbitmq:5672/test",
    ),
    "exchange": os.getenv(
        "DELIVERY_TRIGGER_STARTER_SENDER_EXCHANGE",
        default="notifications_sender.send_delivery",
    ),
}
