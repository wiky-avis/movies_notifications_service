from pydantic import BaseModel


class BaseDaemonConfig(BaseModel):
    run: bool = True
    name: str
    cron: str
