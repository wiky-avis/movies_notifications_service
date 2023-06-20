from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from src.workers.models.delivery import DeliveryChannel


class UserUnsubscriptionModel(BaseModel):
    id: int
    user_id: str
    reason: Optional[str] = None
    channel_type: Optional[DeliveryChannel] = None
    created_dt: Optional[datetime] = None
