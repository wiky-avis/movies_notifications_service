from datetime import datetime
from enum import Enum

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
    email: str | None


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
    created_dt: datetime | None = None
    updated_dt: datetime | None = None


class DeliveryResponse(ORDJSONModelMixin):
    delivery_id: int
    template_id: int | None = None
    recipient: Recipient | None = None
    channel: DeliveryChannel | None = None
    parameters: dict | None = None
    type: DeliveryType | None = None
    sender: str | None = None
    status: DeliveryStatus | None = None
    created_dt: datetime | None = None
    updated_dt: datetime | None = None
