from datetime import datetime
from typing import Optional

from pydantic import Field

from notifications_api.src.api.models.base import ORDJSONModelMixin


class DeliveryModel(ORDJSONModelMixin):
    template_id: int
    recipient: dict
    parameters: dict
    channel: str
    _type: str = Field(alias="type")
    sender: str
    excluded: Optional[bool]
    exclude_reason: Optional[str]
    created_dt: Optional[datetime]
    updated_dt: Optional[datetime]
