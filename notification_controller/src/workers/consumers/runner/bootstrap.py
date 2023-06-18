import punq
from settings.consumers import NotificationsEnricherConfig
from src.common.clients.auth_api import AuthApiClient, resolve_auth_api_client
from src.common.connectors.db import DbConnector
from src.common.repositories.notifications import NotificationsRepository
from src.workers.consumers.notifications_enricher_consumer.consumer import (
    NotificationsEnricherConsumer,
)
from src.workers.consumers.notifications_enricher_consumer.service import (
    NotificationsEnricherService,
)


def resolve_resources(config: NotificationsEnricherConfig) -> punq.Container:
    container = punq.Container()

    container.register(service=DbConnector)
    container.register(
        service=AuthApiClient,
        instance=resolve_auth_api_client(config=config.auth_api_client),
    )
    container.register(service=NotificationsRepository)
    container.register(service=NotificationsEnricherService)
    container.register(
        service=NotificationsEnricherConsumer,
        factory=NotificationsEnricherConsumer,
        config=config.notifications_enricher_consumer,
    )
    return container
