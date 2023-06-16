from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field
from typing_extensions import TypedDict

from notifications_api.src.api.models.base import ORDJSONModelMixin


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
    delivery_id: Optional[int] = None
    status: Optional[DeliveryStatus] = None
    created_dt: Optional[datetime] = None
    updated_dt: Optional[datetime] = None
