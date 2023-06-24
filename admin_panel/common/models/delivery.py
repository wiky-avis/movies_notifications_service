from datetime import datetime
from enum import Enum
from typing import TypedDict

from pydantic import BaseModel, Field


class DeliveryChannel(str, Enum):
    # почта
    EMAIL = "email"


class DeliveryType(str, Enum):
    # сразу
    IMMEDIATELY = "immediately"
    # не ночью
    NOT_NIGHT = "not_night"


class Recipient(TypedDict, total=False):
    user_id: str
    email: str | None


class ObjectParameter(TypedDict):
    name: str
    value: str


class DeliveryModel(BaseModel):
    template_id: int
    recipient: Recipient
    parameters: list[ObjectParameter]
    channel: DeliveryChannel
    type_: DeliveryType = Field(alias="type")
    sender: str
    created_dt: datetime | None = None
    updated_dt: datetime | None = None
