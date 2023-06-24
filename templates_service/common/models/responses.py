from pydantic import BaseModel

from templates_service.common.models.templates import NotificationTemplate


class HTTPErrorResponse(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


class TemplateOut(BaseModel):
    status: str
    template_id: int | None = None
    details: str | None = None


class TemplatesListing(BaseModel):
    status: str
    count: int
    items: list[NotificationTemplate]


class RenderTemplateOut(BaseModel):
    rendered: str
