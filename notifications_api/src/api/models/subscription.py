from enum import Enum

from src.api.models.base import ORDJSONModelMixin


class ChannelType(str, Enum):
    # почта
    EMAIL = "email"


class UserSubscriptionInput(ORDJSONModelMixin):
    user_id: str
    channel_type: ChannelType = ChannelType.EMAIL
    reason: str | None = None
