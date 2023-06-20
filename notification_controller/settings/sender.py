import os

from pydantic import AmqpDsn, BaseSettings


class BaseSenderSettings(BaseSettings):
    run: bool = True
    url: AmqpDsn
    exchange: str


class NotificationsEnricherAmqpSender(BaseSenderSettings):
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
