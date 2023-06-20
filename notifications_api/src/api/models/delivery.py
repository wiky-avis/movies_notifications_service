from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field
from src.api.models.base import ORDJSONModelMixin
from typing_extensions import TypedDict


class EventType(str, Enum):
    CREATED = "created"
    SEND = "send"


class DeliveryStatus(str, Enum):
    # создано
    CREATED = "created"
    # отправлено
    SENT = "sent"
    # не отправлено
    FAILED = "failed"


class DeliveryType(str, Enum):
    # сразу
    IMMEDIATELY = "immediately"
    # не ночью
    NOT_NIGHT = "not_night"


class DeliveryChannel(str, Enum):
    # почта
    EMAIL = "email"


class Recipient(TypedDict, total=False):
    user_id: str
    email: Optional[str]


class ObjectParameter(TypedDict):
    name: str
    value: str


class DeliveryModel(ORDJSONModelMixin):
    template_id: int
    recipient: Recipient
    parameters: list[ObjectParameter]
    channel: DeliveryChannel
    type_: DeliveryType = Field(alias="type")
    sender: str
    created_dt: Optional[datetime] = None
    updated_dt: Optional[datetime] = None


class DeliveryResponse(ORDJSONModelMixin):
    delivery_id: int
    template_id: Optional[int] = None
    recipient: Optional[Recipient] = None
    channel: Optional[DeliveryChannel] = None
    parameters: Optional[dict] = None
    type: Optional[DeliveryType] = None
    sender: Optional[str] = None
    status: Optional[DeliveryStatus] = None
    created_dt: Optional[datetime] = None
    updated_dt: Optional[datetime] = None
