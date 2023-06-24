from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends
from src.api.models.subscription import UserSubscriptionInput
from src.common.responses import ApiResponse, wrap_response
from src.common.services.subscription import UserSubscriptionService
from src.containers import Container


router = APIRouter()


@router.post(
    "/users/unsubscribe",
    summary="Отписка пользователя от коммуникации",
    description="Отписывает переданного пользователя от коммуникации",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def unsubscribe_user(
    body: UserSubscriptionInput = Body(...),
    user_subscription_service: UserSubscriptionService = Depends(
        Provide[Container.user_subscription_service]
    ),
):
    """
    Создает запись в БД в таблице с отписанными пользователями.
    Далее по ней будут фильтроваться отправки.
    """
    return await user_subscription_service.unsubscribe_user(body)
