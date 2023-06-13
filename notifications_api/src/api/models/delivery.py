from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from notifications_api.src.api.models.base import ORDJSONModelMixin


class Recipient(BaseModel):
    user_id: str
    email: Optional[str]


class ObjectParameter(BaseModel):
    value: str
    name: str


class DeliveryModel(ORDJSONModelMixin):
    template_id: int
    recipient: Recipient
    parameters: dict[ObjectParameter]  # type: ignore[type-arg]
    channel: str
    type_: str = Field(alias="type")
    sender: str
    excluded: Optional[bool]
    exclude_reason: Optional[str]
    created_dt: Optional[datetime]
    updated_dt: Optional[datetime]
