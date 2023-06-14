from dependency_injector import containers, providers

from notifications_api.src.common.connectors import db
from notifications_api.src.common.repositories.notifications import (
    NotificationsRepository,
)
from notifications_api.src.common.services.notifications import (
    NotificationsService,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "notifications_api.src.api.srv.endpoints.deliveries",
        ]
    )

    db_client = providers.Factory(db.DbConnector)

    notifications_repository = providers.Factory(
        NotificationsRepository,
        db=db_client,
    )

    notifications_service = providers.Factory(
        NotificationsService,
        repository=notifications_repository,
    )
