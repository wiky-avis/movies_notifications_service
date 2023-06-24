from http import HTTPStatus

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from src.api.models.subscription import UserSubscriptionInput
from src.common.exceptions import DatabaseError
from src.common.repositories.notifications import NotificationsRepository


class UserSubscriptionService:
    def __init__(
        self,
        repository: NotificationsRepository,
    ):
        self._repository = repository

    async def unsubscribe_user(
        self, data: UserSubscriptionInput
    ) -> str | None:
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
