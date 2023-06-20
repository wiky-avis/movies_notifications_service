import logging

from src.common.connectors.db import DbConnector
from src.common.repositories import queries
from src.workers.models.delivery import DeliveryModel
from src.workers.models.recipient import UserUnsubscriptionModel


logger = logging.getLogger(__name__)


class NotificationsRepository:
    def __init__(self, db: DbConnector):
        self._db = db

    async def _get_delivery_data(self, delivery_id: int):
        row_data = await self._db.pool.fetchrow(  # type: ignore[union-attr]
            queries.GET_DELIVERY, delivery_id
        )
        return DeliveryModel.parse_obj(row_data) if row_data else None

    async def set_excluded_delivery(
        self, exclude_reason: str, delivery_id: int
    ):
        return await self._db.pool.execute(
            queries.SET_EXCLUDED_DELIVERY, exclude_reason, delivery_id
        )

    async def check_user_subscription(self, user_id: str):
        row_data = await self._db.pool.fetchrow(  # type: ignore[union-attr]
            queries.GET_USER_UNSUBSCRIPTION, user_id
        )
        return (
            UserUnsubscriptionModel.parse_obj(row_data) if row_data else None
        )
