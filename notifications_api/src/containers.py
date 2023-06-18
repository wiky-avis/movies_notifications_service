from dependency_injector import containers, providers

from notifications_api.src.common.connectors import amqp, db
from notifications_api.src.common.repositories.notifications import (
    NotificationsRepository,
)
from notifications_api.src.common.services.notifications import (
    NotificationsService,
)
from notifications_api.src.common.services.subscription import (
    UserSubscriptionService,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "notifications_api.src.api.srv.endpoints.deliveries",
            "notifications_api.src.api.v1.endpoints.users",
        ]
    )

    db_client = providers.Factory(db.DbConnector)
    amqp_client = providers.Factory(amqp.AMQPSenderPikaConnector)

    notifications_repository = providers.Factory(
        NotificationsRepository, db=db_client
    )

    notifications_service = providers.Factory(
        NotificationsService,
        repository=notifications_repository,
        amqp_pika_sender=amqp_client,
    )

    user_subscription_service = providers.Factory(
        UserSubscriptionService,
        repository=notifications_repository,
    )
