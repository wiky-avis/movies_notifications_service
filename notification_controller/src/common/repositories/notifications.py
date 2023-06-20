import logging
from typing import Optional

from src.common.connectors.db import DbConnector
from src.common.repositories import queries
from src.workers.models.delivery import DeliveryModel, DeliveryStatus
from src.workers.models.recipient import UserUnsubscriptionModel


logger = logging.getLogger(__name__)


class NotificationsRepository:
    def __init__(self, db: DbConnector):
        self._db = db

    async def get_delivery_data(self, delivery_id: int) -> DeliveryModel:
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

    async def update_delivery(
        self, recipient: dict, tz: str, delivery_id: int
    ):
        return await self._db.pool.execute(
            queries.UPDATE_DELIVERY, recipient, tz, delivery_id
        )

    async def check_user_unsubscription(
        self, user_id: str
    ) -> UserUnsubscriptionModel:
        row_data = await self._db.pool.fetchrow(  # type: ignore[union-attr]
            queries.GET_USER_UNSUBSCRIPTION, user_id
        )
        return (
            UserUnsubscriptionModel.parse_obj(row_data) if row_data else None
        )

    async def create_delivery_distribution(self, delivery_data: DeliveryModel):
        return await self._db.pool.execute(
            queries.CREATE_DELIVERY_DISTRIBUTION,
            delivery_data.delivery_id,
            delivery_data.recipient,
            DeliveryStatus.CREATED,
        )

    async def set_delivery_distribution_status(
        self, status: str, delivery_id: int, errors: Optional[dict] = None
    ):
        return await self._db.pool.execute(
            queries.SET_DISTRIBUTIONS_STATUS, status, errors, delivery_id
        )
