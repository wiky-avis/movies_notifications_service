import logging
from typing import Optional

from notifications_api.src.api.models.delivery import (
    DeliveryModel,
    DeliveryResponse,
)
from notifications_api.src.common.connectors.db import DbConnector
from notifications_api.src.common.exceptions import DatabaseError
from notifications_api.src.common.repositories import queries


logger = logging.getLogger(__name__)


class NotificationsRepository:
    def __init__(self, db: DbConnector):
        self._db = db

    async def create_delivery(
        self, data: DeliveryModel
    ) -> Optional[DeliveryResponse]:
        parameters = {
            parameter["name"]: parameter["value"]
            for parameter in data.parameters
        }
        try:
            row_data = await self._db.pool.fetchrow(  # type: ignore[union-attr]
                queries.CREATE_DELIVERY,
                data.template_id,
                data.recipient,
                parameters,
                data.channel,
                data.type_,
                data.sender,
            )
        except Exception:
            logger.exception(
                "Failed to create a new delivery: template_id %s recipient %s channel %s sender %s",
                data.template_id,
                data.recipient,
                data.channel,
                data.sender,
                exc_info=True,
            )
            raise DatabaseError()
        return DeliveryResponse.parse_obj(row_data) if row_data else None

    async def get_delivery_by_id(
        self, delivery_id: int
    ) -> Optional[DeliveryResponse]:
        row_data = await self._db.pool.fetchrow(  # type: ignore[union-attr]
            queries.GET_DELIVERY, delivery_id
        )
        return DeliveryResponse.parse_obj(row_data) if row_data else None
