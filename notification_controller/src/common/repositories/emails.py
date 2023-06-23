import logging
from typing import Optional

from src.common.connectors.db import DbConnector
from src.common.repositories import queries
from src.workers.models.emails import EmailForSend


logger = logging.getLogger(__name__)


class EmailRepository:
    def __init__(self, db: DbConnector):
        self._db = db

    async def get_delivery_for_send(self, delivery_id: int) -> EmailForSend:
        row_data = await self._db.pool.fetchrow(  # type: ignore[union-attr]
            queries.GET_DELIVERY_FOR_SEND, delivery_id
        )
        return EmailForSend.parse_obj(row_data) if row_data else None

    async def set_excluded_delivery(
        self, exclude_reason: str, delivery_id: int
    ):
        """
        Вызывается при успешной отправке имейла
        """
        return await self._db.pool.execute(
            queries.SET_EXCLUDED_DELIVERY, exclude_reason, delivery_id
        )

    async def set_delivery_distribution_status(
        self, status: str, delivery_id: int, errors: Optional[dict] = None
    ):
        """
        Статус меняется при успешной отправке на sent
        А при ошибке на failed
        """
        return await self._db.pool.execute(
            queries.SET_DISTRIBUTIONS_STATUS, status, errors, delivery_id
        )
