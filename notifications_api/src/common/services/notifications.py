from http import HTTPStatus

from fastapi import HTTPException
from starlette.responses import JSONResponse

from notifications_api.src.api.models.delivery import (
    DeliveryModel,
    DeliveryResponse,
)
from notifications_api.src.common.exceptions import DatabaseError
from notifications_api.src.common.repositories.notifications import (
    NotificationsRepository,
)


class NotificationsService:
    def __init__(self, repository: NotificationsRepository):
        self._repository = repository

    async def create_delivery(self, data: DeliveryModel):
        try:
            delivery_id = await self._repository.create_delivery(data)
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create a new delivery.",
            )
        return JSONResponse(
            content=DeliveryResponse(delivery_id=delivery_id).dict(
                exclude_none=True
            )
        )
