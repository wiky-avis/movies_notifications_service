from fastapi import APIRouter

from notifications_api.src.api.srv.endpoints import deliveries, technical


router = APIRouter(prefix="/api/srv", tags=["srv"])

router.include_router(deliveries.router)
router.include_router(technical.router)
