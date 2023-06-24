from datetime import datetime

from pydantic import BaseModel
from src.workers.models.delivery import DeliveryChannel


class UserUnsubscriptionModel(BaseModel):
    id: int
    user_id: str
    reason: str | None = None
    channel_type: DeliveryChannel | None = None
    created_dt: datetime | None = None
