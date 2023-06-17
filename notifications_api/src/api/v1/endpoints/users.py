from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends

from notifications_api.src.api.models.subscription import UserSubscriptionInput
from notifications_api.src.common.responses import ApiResponse, wrap_response
from notifications_api.src.common.services.subscription import (
    UserSubscriptionService,
)
from notifications_api.src.containers import Container


router = APIRouter()


@router.post("/users/unsubscribe", response_model=ApiResponse)
@inject
@wrap_response
async def unsubscribe_user(
    body: UserSubscriptionInput = Body(...),
    user_subscription_service: UserSubscriptionService = Depends(
        Provide[Container.user_subscription_service]
    ),
):
    return await user_subscription_service.unsubscribe_user(body)
