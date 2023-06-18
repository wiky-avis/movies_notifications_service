from enum import Enum
from typing import Dict, Optional

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
    template_id: Optional[int] = None
    template_name: str
    template_body: str
    description: Optional[str] = None
    mandatory_parameters: Optional[list[str]] = None
    optional_parameters: Optional[Dict[str, str]] = None
    channel: DeliveryChannel
    type_: DeliveryType = Field(alias="type", default=DeliveryType.REGULAR)
