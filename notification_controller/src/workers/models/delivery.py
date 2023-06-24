from datetime import datetime
from enum import Enum

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
    template_id: int | None = None
    recipient: dict | None = None
    channel: DeliveryChannel | None = None
    parameters: dict | None = None
    type: DeliveryType | None = None
    sender: str | None = None
    status: str | None = None
    created_dt: datetime | None = None
    updated_dt: datetime | None = None


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


class ReadyToSendDeliveryModel(BaseModel):
    delivery_id: int
    recipient: dict | None = None
