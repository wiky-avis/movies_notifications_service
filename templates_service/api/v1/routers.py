from fastapi import APIRouter

from templates_service.api.v1.endpoints import templates


router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(templates.router)
