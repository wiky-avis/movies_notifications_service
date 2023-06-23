from typing import Optional

from pydantic import BaseModel


class EmailRecipient(BaseModel):
    user_id: str
    email: str


class EmailForSend(BaseModel):
    delivery_id: int
    template_id: int
    recipient: EmailRecipient
    parameters: Optional[dict] = {}
    sender: str
