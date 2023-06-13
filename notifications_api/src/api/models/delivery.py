from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeliveryModel(BaseModel):
    template_id: int
    recipient: dict
    parameters: dict
    channel: str
    _type: str
    sender: str
    excluded: Optional[bool]
    exclude_reason: Optional[str]
    created_dt: Optional[datetime]
    updated_dt: Optional[datetime]
