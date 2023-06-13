from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException

from notifications_api.src.common.connectors.db import get_db
from notifications_api.src.settings import token_settings


router = APIRouter()


@router.post(
    "/v1/deliveries",
)
async def create_delivery(
    token_header: Optional[str] = Header(
        None, alias=token_settings.token_header
    ),
    db=Depends(get_db),
):
    pass
