from typing import Optional

from notifications_api.src.api.models.base import ORDJSONModelMixin


class UserSubscriptionInput(ORDJSONModelMixin):
    user_id: str
    reason: Optional[str] = None
