import logging
from typing import Optional

import dpath
from pydantic import ValidationError
from src.common.clients.auth_api import AuthApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.exceptions import BadRequestError, ClientError, ServiceError
from src.common.repositories.notifications import NotificationsRepository
from src.workers.models.delivery import DeliveryEventModel

from notification_controller.src.workers.models.delivery import (
    DeliveryModel,
    DeliveryStatus,
    DeliveryType,
    EventType,
    ExcludeReasonEnum,
)


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

    async def main(self, body: bytes) -> None:
        delivery_event = self._load_model(body)
        print("---DELIVERY", delivery_event)

        delivery_data = await self._repository._get_delivery_data(
            delivery_id=delivery_event.delivery_id
        )
        if not delivery_data:
            logger.warning(
                "Delivery no found: delivery_id %s",
                delivery_event.delivery_id,
                exc_info=True,
            )
            return

        await self._enrich_delivery_data(delivery_data)

        if delivery_data.type == DeliveryType.IMMEDIATELY:
            await self._repository.create_delivery_distribution(delivery_data)
            await self.send_message(delivery_data.delivery_id)

    async def _enrich_delivery_data(self, delivery_data: DeliveryModel):
        recipient_id = dpath.get(delivery_data.recipient, "user_id", default=None)
        user_unsubscribed = await self._repository.check_user_unsubscription(
            recipient_id
        )
        if user_unsubscribed:
            await self._repository.set_excluded_delivery(
                exclude_reason=ExcludeReasonEnum.USER_UNSUBSCRIBED,
                delivery_id=delivery_data.delivery_id,
            )
            return

        user_info = await self.get_user_info(recipient_id)  # type: ignore[arg-type]
        if not user_info:
            logger.warning(
                "User no found: recipient_id %s",
                recipient_id,
                exc_info=True,
            )
            return

        email = dpath.get(delivery_data.recipient, "email", default=None)
        if not email:
            email = dpath.get(user_info, "email", default=None)
            delivery_data.recipient.update(dict(email=email))

        tz = dpath.get(user_info, "tz", default=None)

        await self._repository.update_delivery(
            delivery_data.recipient, tz, delivery_data.delivery_id
        )

    async def get_user_info(self, recipient_id: str):
        try:
            user = self._auth_api_client.get_user_by_id(recipient_id)
        except (BadRequestError, ServiceError, ClientError):
            logger.warning(
                "Getting user info error: user_id %s",
                recipient_id,
                exc_info=True,
            )
            return
        return user

    async def send_message(self, delivery_id: int) -> None:
        try:
            await self._amqp_pika_sender.amqp_sender.send(  # type: ignore
                message={
                    "delivery_id": delivery_id,
                    "event": EventType.SEND,
                },
                routing_key="event.send",
            )
        except Exception:
            logger.exception(
                "Fail to send message: delivery_id %s",
                delivery_id,
                exc_info=True,
            )
            await self._repository.create_delivery_distribution(
                delivery_id, DeliveryStatus.FAILED
            )

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
