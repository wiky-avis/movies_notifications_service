import logging
from typing import Optional

from pydantic import ValidationError
from src.common.clients.auth_api import AuthApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.repositories.notifications import NotificationsRepository
from src.workers.models.delivery import DeliveryEventModel


logger = logging.getLogger(__name__)


class NotificationsEnricherService:
    def __init__(
        self,
        repository: NotificationsRepository,
        auth_api_client: AuthApiClient,
        amqp_sender: AMQPSenderPikaConnector,
    ):
        self._repository = repository
        self._auth_api_client = auth_api_client
        self._amqp_sender = amqp_sender

    async def main(self, body: bytes):
        delivery_event = self._load_model(body)
        print("---DELIVERY", delivery_event)

        delivery_data = await self._repository._get_delivery_data(
            delivery_id=delivery_event.delivery_id
        )
        if not delivery_data:
            return

    @staticmethod
    def _load_model(
        body: bytes,
    ) -> Optional[DeliveryEventModel]:
        try:
            return DeliveryEventModel.parse_raw(body)
        except ValidationError:
            logger.warning(
                "Fail to parse data for notifications event - %s",
                body,
                exc_info=True,
            )
