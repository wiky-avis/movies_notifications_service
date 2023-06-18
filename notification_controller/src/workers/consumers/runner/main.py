from settings import (
    AUTH_API_SERVICE,
    NOTIFICATIONS_ENRICHER_CONSUMER,
    NotificationsEnricherConfig,
)
from src.workers.consumers.runner import application, bootstrap


config = NotificationsEnricherConfig(
    auth_api_client=AUTH_API_SERVICE,
    notifications_enricher_consumer=NOTIFICATIONS_ENRICHER_CONSUMER,
)

resources = bootstrap.resolve_resources(config=config)

resources.register(application.Runner)

consumers = resources.resolve(application.Runner).consumers
