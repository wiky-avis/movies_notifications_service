from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EventType(str, Enum):
    CREATED = "created"
    SEND = "send"


class DeliveryEventModel(BaseModel):
    delivery_id: int
    event: EventType = EventType.CREATED


class DeliveryType(str, Enum):
    # сразу
    IMMEDIATELY = "immediately"
    # не ночью
    NOT_NIGHT = "not_night"


class DeliveryChannel(str, Enum):
    # почта
    EMAIL = "email"


class DeliveryModel(BaseModel):
    delivery_id: int
    template_id: Optional[int] = None
    recipient: Optional[dict] = None
    channel: Optional[DeliveryChannel] = None
    parameters: Optional[dict] = None
    type: Optional[DeliveryType] = None
    sender: Optional[str] = None
    status: Optional[str] = None
    created_dt: Optional[datetime] = None
    updated_dt: Optional[datetime] = None


class ExcludeReasonEnum(str, Enum):
    # Пользователь отписался от рассылок
    USER_UNSUBSCRIBED = "user_unsubscribed"


class DeliveryStatus(str, Enum):
    # создано
    CREATED = "created"
    # отправлено
    SENT = "sent"
    # не отправлено
    FAILED = "failed"
