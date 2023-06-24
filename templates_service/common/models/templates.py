from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field


class DeliveryType(str, Enum):
    # сразу
    FAST = "immediately"
    # не ночью
    REGULAR = "not_night"


class DeliveryChannel(str, Enum):
    # почта
    EMAIL = "email"


class NotificationTemplate(BaseModel):
    template_id: int | None = None
    template_name: str
    template_body: str
    description: str | None = None
    mandatory_parameters: list[str] | None = None
    optional_parameters: Dict[str, str] | None = None
    channel: DeliveryChannel
    type_: DeliveryType = Field(alias="type", default=DeliveryType.REGULAR)
