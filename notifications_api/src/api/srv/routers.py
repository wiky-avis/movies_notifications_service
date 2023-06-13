from fastapi import APIRouter

from notifications_api.src.api.srv.endpoints import deliveries

router = APIRouter(prefix="/api/srv", tags=["srv"])

router.include_router(deliveries.router)
