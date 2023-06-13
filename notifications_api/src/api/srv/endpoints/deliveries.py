from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from starlette import status

from notifications_api.src.api.models.delivery import DeliveryModel
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
    body: DeliveryModel = Body(
        example='{"template_id": 123,'
        '"recipient": {"user_id": "gf2536254"},'
        '"parameters": ['
        '{"name": "subject", "value": "Приветственное письмо"},'
        '{"name": "username", "value": "vasya"}'
        "],"
        '"channel": "email", "type": "not_at_night", "sender": "ugs_service"}',
    ),
    notifications_service: NotificationsService = Depends(
        Provide[Container.notifications_service]
    ),
):
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in NOTIFICATIONS_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    print(body)

    return body.dict()
