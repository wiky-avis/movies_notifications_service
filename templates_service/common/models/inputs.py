from typing import Optional

from pydantic import BaseModel, Field

from templates_service.common.models.templates import (
    DeliveryChannel,
    DeliveryType,
)


class CreateTemplateIn(BaseModel):
    template_id: Optional[int] = None
    template_name: str
    template_body: str
    description: Optional[str] = None
    channel: DeliveryChannel
    type_: DeliveryType = Field(alias="type", default=DeliveryType.REGULAR)
