from enum import Enum, IntEnum


class Status(IntEnum):
    on = 1
    off = 0


class NotificationStatus(str, Enum):
    active = "active"
    delete = "delete"
    edit = "edit"


class Action(str, Enum):
    create = "create"
    delete = "delete"
    edit = "edit"
