from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends
from src.api.models.subscription import UserSubscriptionInput
from src.common.responses import ApiResponse, wrap_response
from src.common.services.subscription import UserSubscriptionService
from src.containers import Container


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
