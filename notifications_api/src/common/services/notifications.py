from notifications_api.src.common.repositories.notifications import (
    NotificationsRepository,
)


class NotificationsService:
    def __init__(self, repository: NotificationsRepository):
        self._repository = repository
