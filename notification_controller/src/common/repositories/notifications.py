import logging

from src.common.connectors.db import DbConnector
from src.common.repositories import queries
from src.workers.models.delivery import DeliveryModel


logger = logging.getLogger(__name__)


class NotificationsRepository:
    def __init__(self, db: DbConnector):
        self._db = db

    async def _get_delivery_data(self, delivery_id: int):
        row_data = await self._db.pool.fetchrow(  # type: ignore[union-attr]
            queries.GET_DELIVERY, delivery_id
        )
        return DeliveryModel.parse_obj(row_data) if row_data else None
