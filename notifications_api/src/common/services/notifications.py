import logging
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from src.api.models.delivery import DeliveryModel, DeliveryResponse, EventType
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.exceptions import DatabaseError
from src.common.repositories.notifications import NotificationsRepository
from src.settings import notifications_amqp_settings
from starlette import status


logger = logging.getLogger(__name__)


class NotificationsService:
    def __init__(
        self,
        repository: NotificationsRepository,
        amqp_pika_sender: AMQPSenderPikaConnector,
    ):
        self._repository = repository
        self._amqp_pika_sender = amqp_pika_sender

    async def create_delivery(
        self, data: DeliveryModel
    ) -> Optional[DeliveryResponse]:
        try:
            delivery = await self._repository.create_delivery(data)
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create a new delivery.",
            )
        await self.send_message(delivery.delivery_id)  # type: ignore
        return delivery

    async def send_message(self, delivery_id: int) -> None:
        try:
            await self._amqp_pika_sender.amqp_sender.send(  # type: ignore
                message={
                    "delivery_id": delivery_id,
                    "event": EventType.CREATED,
                },
                exchange=notifications_amqp_settings.exchange,
                routing_key=notifications_amqp_settings.routing_key,
            )
        except Exception:
            logger.exception(
                "Fail to send message: delivery_id %s",
                delivery_id,
                exc_info=True,
            )

    async def get_delivery_by_id(
        self, delivery_id: int
    ) -> Optional[DeliveryResponse]:
        delivery = await self._repository.get_delivery_by_id(delivery_id)
        if not delivery:
            logger.warning(
                "Delivery not found: delivery_id %s",
                delivery_id,
                exc_info=True,
            )
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Delivery not found"
            )
        return delivery
