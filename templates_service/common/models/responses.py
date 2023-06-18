from typing import Optional

from pydantic import BaseModel


class CreateTemplateOut(BaseModel):
    status: str
    details: Optional[str] = None


class HTTPErrorResponse(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
