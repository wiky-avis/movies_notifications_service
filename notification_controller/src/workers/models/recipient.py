from typing import Optional

from pydantic import BaseModel


class Recipient(BaseModel):
    user_id: str
    email: Optional[str] = None
