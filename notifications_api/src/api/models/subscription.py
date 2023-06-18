from enum import Enum
from typing import Optional

from notifications_api.src.api.models.base import ORDJSONModelMixin


class MailingType(str, Enum):
    # почта
    EMAIL = "email"


class UserSubscriptionInput(ORDJSONModelMixin):
    user_id: str
    mailing_type: MailingType = MailingType.EMAIL
    reason: Optional[str] = None
