import logging

from settings import FROM_TZ, TO_TZ
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.repositories.notifications import NotificationsRepository
from src.workers.models.delivery import (
    DeliveryModel,
    DeliveryStatus,
    EventType,
)


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
        deliveries = await self.get_deliveries(from_tz=FROM_TZ, to_tz=TO_TZ)
        for delivery in deliveries:
            await self.create_distribution(delivery)
            await self.send_message(delivery.delivery_id)

    async def get_deliveries(self, from_tz: int, to_tz: int):
        deliveries = await self._repository.get_ready_to_send_deliveries(
            from_tz=from_tz, to_tz=to_tz
        )
        if not deliveries:
            logger.warning("Deliveries not found", exc_info=True)
            return

        return deliveries

    async def create_distribution(self, delivery_data: DeliveryModel):
        await self._repository.create_delivery_distribution(
            delivery_data=delivery_data
        )

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
            errors = dict(delivery_trigger_starter_amqp_sender=str(error))
            logger.exception(
                "Fail to send message: delivery_id %s",
                delivery_id,
                exc_info=True,
            )
            await self._repository.set_delivery_distribution_status(
                status=DeliveryStatus.FAILED,
                delivery_id=delivery_id,
                errors=errors,
            )
