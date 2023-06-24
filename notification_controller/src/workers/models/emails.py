from pydantic import BaseModel


class EmailRecipient(BaseModel):
    user_id: str
    email: str


class EmailForSend(BaseModel):
    delivery_id: int
    template_id: int
    recipient: EmailRecipient
    parameters: dict | None = {}
    sender: str
