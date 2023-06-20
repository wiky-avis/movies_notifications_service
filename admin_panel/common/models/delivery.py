from datetime import datetime
from enum import Enum
from typing import Optional, TypedDict

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
    email: Optional[str]


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
    created_dt: Optional[datetime] = None
    updated_dt: Optional[datetime] = None
