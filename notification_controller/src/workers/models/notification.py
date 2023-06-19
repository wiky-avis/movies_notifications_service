from pydantic import BaseModel


class NotificationEventModel(BaseModel):
    delivery_id: int
