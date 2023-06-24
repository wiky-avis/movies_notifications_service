from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel, Field

from templates_service.common.models.templates import (
    DeliveryChannel,
    DeliveryType,
)


class SearchMode(str, Enum):
    EQUALS = "equals"
    CONTAINS = "contains"
    ALL = "all"


class SearchField(str, Enum):
    TEMPLATE_ID = "template_id"
    TEMPLATE_NAME = "template_name"


class CreateTemplateIn(BaseModel):
    template_name: str
    template_body: str
    description: str | None = None
    channel: DeliveryChannel
    type_: DeliveryType = Field(alias="type", default=DeliveryType.REGULAR)


class UpdateTemplateIn(BaseModel):
    template_id: int
    template_name: str | None = None
    template_body: str | None = None
    description: str | None = None
    channel: DeliveryChannel | None = None
    type_: DeliveryType | None = Field(alias="type", default=None)


class GetTemplateIn(BaseModel):
    search_field: SearchField = SearchField.TEMPLATE_ID
    search_query: str = "Undefined"
    search_mode: SearchMode = SearchMode.EQUALS


class RenderTemplateIn(BaseModel):
    template_id: int
    parameters: Dict[str, Any] = {}
