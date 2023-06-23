import punq
from settings.consumers import ConsumersConfig
from src.common.clients.auth_api import AuthApiClient, resolve_auth_api_client
from src.common.clients.template_api import (
    TemplateApiClient,
    resolve_template_api_client,
)
from src.common.connectors.amqp import (
    AMQPSenderPikaConnector,
    resolve_amqp_sender_client,
)
from src.common.connectors.db import DbConnector
from src.common.repositories.emails import EmailRepository
from src.common.repositories.notifications import NotificationsRepository
from src.workers.consumers.email_consumer.consumer import EmailConsumer
from src.workers.consumers.email_consumer.service import EmailService
from src.workers.consumers.notifications_enricher_consumer.consumer import (
    NotificationsEnricherConsumer,
)
from src.workers.consumers.notifications_enricher_consumer.service import (
    NotificationsEnricherService,
)


def resolve_resources(config: ConsumersConfig) -> punq.Container:
    container = punq.Container()

    container.register(service=DbConnector)
    container.register(
        service=AuthApiClient,
        instance=resolve_auth_api_client(config=config.auth_api_client),
    )
    container.register(
        service=TemplateApiClient,
        instance=resolve_template_api_client(
            config=config.template_api_client
        ),
    )
    container.register(
        service=AMQPSenderPikaConnector,
        instance=resolve_amqp_sender_client(
            config=config.notifications_enricher_amqp_sender
        ),
    )
    container.register(service=NotificationsRepository)
    container.register(service=NotificationsEnricherService)
    container.register(
        service=NotificationsEnricherConsumer,
        factory=NotificationsEnricherConsumer,
        config=config.notifications_enricher_consumer,
    )
    container.register(service=EmailRepository)
    container.register(service=EmailService)
    container.register(
        service=EmailConsumer,
        factory=EmailConsumer,
        config=config.email_consumer,
    )
    return container
