import logging

from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.repositories.notifications import NotificationsRepository


logger = logging.getLogger(__name__)


class DeliveryTriggerStarterService:
    def __init__(
        self,
        repository: NotificationsRepository,
        amqp_sender: AMQPSenderPikaConnector,
    ):
        self._repository = repository
        self._amqp_sender = amqp_sender

    async def main(self) -> None:
        pass
