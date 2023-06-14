from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field
from typing_extensions import TypedDict

from notifications_api.src.api.models.base import ORDJSONModelMixin


class DeliveryType(str, Enum):
    # сразу
    CREATED = "immediately"
    # не ночью
    SENT = "not_night"


class DeliveryChannel(str, Enum):
    # почта
    EMAIL = "email"


class Recipient(TypedDict, total=False):
    user_id: str
    email: Optional[str]


class ObjectParameter(TypedDict):
    value: str
    name: str


class DeliveryModel(ORDJSONModelMixin):
    template_id: int
    recipient: Recipient
    parameters: list[ObjectParameter]
    channel: DeliveryChannel
    type_: DeliveryType = Field(alias="type")
    sender: str
    excluded: Optional[bool]
    exclude_reason: Optional[str]
    created_dt: Optional[datetime]
    updated_dt: Optional[datetime]


class DeliveryResponse(ORDJSONModelMixin):
    delivery_id: Optional[int]
