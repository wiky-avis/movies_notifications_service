from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from starlette import status

from notifications_api.src.api.models.delivery import (
    DeliveryModel,
    DeliveryResponse,
)
from notifications_api.src.common.services.notifications import (
    NotificationsService,
)
from notifications_api.src.containers import Container
from notifications_api.src.settings import token_settings
from notifications_api.src.settings.token import NOTIFICATIONS_SRV_TOKENS


router = APIRouter()


@router.post(
    "/v1/deliveries",
)
@inject
async def create_delivery(
    token_header: Optional[str] = Header(
        None, alias=token_settings.token_header
    ),
    body: DeliveryModel = Body(...),
    notifications_service: NotificationsService = Depends(
        Provide[Container.notifications_service]
    ),
) -> DeliveryResponse:
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in NOTIFICATIONS_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await notifications_service.create_delivery(body)


@router.get(
    "/v1/deliveries/{delivery_id}",
)
@inject
async def get_delivery(
    delivery_id: int,
    token_header: Optional[str] = Header(
        None, alias=token_settings.token_header
    ),
    notifications_service: NotificationsService = Depends(
        Provide[Container.notifications_service]
    ),
) -> DeliveryResponse:
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in NOTIFICATIONS_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await notifications_service.get_delivery_by_id(delivery_id)
