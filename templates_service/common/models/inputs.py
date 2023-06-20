from enum import Enum
from typing import Any, Dict, Optional

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
    description: Optional[str] = None
    channel: DeliveryChannel
    type_: DeliveryType = Field(alias="type", default=DeliveryType.REGULAR)


class UpdateTemplateIn(BaseModel):
    template_id: int
    template_name: Optional[str] = None
    template_body: Optional[str] = None
    description: Optional[str] = None
    channel: Optional[DeliveryChannel] = None
    type_: Optional[DeliveryType] = Field(alias="type", default=None)


class GetTemplateIn(BaseModel):
    search_field: SearchField = SearchField.TEMPLATE_ID
    search_query: str = "Undefined"
    search_mode: SearchMode = SearchMode.EQUALS


class RenderTemplateIn(BaseModel):
    template_id: int
    parameters: Dict[str, Any] = {}
