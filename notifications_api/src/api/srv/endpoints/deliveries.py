from fastapi import APIRouter, Body, Depends, HTTPException

from notifications_api.src.common.connectors.db import get_db

router = APIRouter()


@router.post(
    "/v1/deliveries",
)
async def create_deliveries(
    db=Depends(get_db),
):
    pass
