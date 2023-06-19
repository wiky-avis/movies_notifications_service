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
        default="amqp://user:pass@127.0.0.1:8030/test",
    ),
    "exchange": os.getenv(
        "NOTIFICATIONS_ENRICHER_SENDER_EXCHANGE", default="notifications"
    ),
}
