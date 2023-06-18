from http import HTTPStatus
from typing import Optional

from asyncpg import UniqueViolationError
from fastapi import HTTPException

from notifications_api.src.api.models.subscription import UserSubscriptionInput
from notifications_api.src.common.exceptions import DatabaseError
from notifications_api.src.common.repositories.notifications import (
    NotificationsRepository,
)


class UserSubscriptionService:
    def __init__(
        self,
        repository: NotificationsRepository,
    ):
        self._repository = repository

    async def unsubscribe_user(
        self, data: UserSubscriptionInput
    ) -> Optional[str]:
        try:
            await self._repository.unsubscribe_user(data)
        except UniqueViolationError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="The user has already been unsubscribed.",
            )
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create unsubscribe.",
            )
        return "Ok"
