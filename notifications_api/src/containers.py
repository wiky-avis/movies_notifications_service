from dependency_injector import containers, providers
from src.common.connectors import amqp, db
from src.common.repositories.notifications import NotificationsRepository
from src.common.services.notifications import NotificationsService
from src.common.services.subscription import UserSubscriptionService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.srv.endpoints.deliveries",
            "src.api.v1.endpoints.users",
        ]
    )

    db_client = providers.Factory(db.DbConnector)  # type: ignore
    amqp_client = providers.Factory(amqp.AMQPSenderPikaConnector)  # type: ignore

    notifications_repository = providers.Factory(  # type: ignore
        NotificationsRepository, db=db_client
    )

    notifications_service = providers.Factory(  # type: ignore
        NotificationsService,
        repository=notifications_repository,
        amqp_pika_sender=amqp_client,
    )

    user_subscription_service = providers.Factory(  # type: ignore
        UserSubscriptionService,
        repository=notifications_repository,
    )
