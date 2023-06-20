import logging
from typing import Optional

import dpath
from pydantic import ValidationError
from src.common.clients.auth_api import AuthApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.exceptions import BadRequestError, ClientError, ServiceError
from src.common.repositories.notifications import NotificationsRepository
from src.workers.models.delivery import (
    DeliveryEventModel,
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

        delivery_data = await self._repository.get_delivery_data(
            delivery_id=delivery_event.delivery_id
        )
        if not delivery_data:
            logger.warning(
                "Delivery not found: delivery_id %s",
                delivery_event.delivery_id,
                exc_info=True,
            )
            return

        await self._enrich_delivery_data(delivery_data)

        if delivery_data.type == DeliveryType.IMMEDIATELY:
            await self._repository.create_delivery_distribution(delivery_data)
            await self.send_message(delivery_data.delivery_id)

    async def _enrich_delivery_data(
        self, delivery_data: DeliveryModel
    ) -> None:
        recipient_id = dpath.get(
            delivery_data.recipient, "user_id", default=None
        )
        user_unsubscribed = await self._repository.check_user_unsubscription(
            recipient_id
        )
        if user_unsubscribed:
            await self._repository.set_excluded_delivery(
                exclude_reason=ExcludeReasonEnum.USER_UNSUBSCRIBED,
                delivery_id=delivery_data.delivery_id,
            )
            logger.warning(
                "Excluded delivery %s. User unsubscribed: recipient_id %s, reason %s channel_type %s",
                delivery_data.delivery_id,
                recipient_id,
                user_unsubscribed.reason,
                user_unsubscribed.channel_type,
            )
            return

        user_info = await self.get_user_info(recipient_id)  # type: ignore[arg-type]
        if not user_info:
            logger.warning(
                "User not found: user_id %s",
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

    async def get_user_info(self, user_id: str) -> Optional[dict]:
        try:
            user = await self._auth_api_client.get_user_by_id(user_id)
        except (BadRequestError, ServiceError, ClientError):
            logger.warning(
                "Getting user info error: user_id %s",
                user_id,
                exc_info=True,
            )
            return
        return user

    async def send_message(self, delivery_id: int) -> None:
        try:
            await self._amqp_sender.amqp_sender.send(  # type: ignore
                message={
                    "delivery_id": delivery_id,
                    "event": EventType.SEND,
                },
                routing_key="event.send",
            )
        except Exception as error:
            errors = dict(notifications_enricher_amqp_sender=str(error))
            logger.exception(
                "Fail to send message: delivery_id %s",
                delivery_id,
                exc_info=True,
            )
            await self._repository.set_delivery_distribution_status(
                delivery_id, DeliveryStatus.FAILED, errors
            )

    @staticmethod
    def _load_model(
        body: bytes,
    ) -> Optional[DeliveryEventModel]:
        try:
            return DeliveryEventModel.parse_raw(body)
        except ValidationError:
            logger.warning(
                "Fail to parse data for delivery event - %s",
                body,
                exc_info=True,
            )
