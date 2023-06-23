from settings import (
    AUTH_API_SERVICE,
    EMAIL_CONSUMER,
    NOTIFICATIONS_ENRICHER_CONSUMER,
    TEMPLATES_API_SERVICE,
    ConsumersConfig,
)
from settings.sender import NOTIFICATIONS_ENRICHER_SENDER
from src.workers.consumers.runner import application, bootstrap


config = ConsumersConfig(
    auth_api_client=AUTH_API_SERVICE,
    notifications_enricher_consumer=NOTIFICATIONS_ENRICHER_CONSUMER,
    notifications_enricher_amqp_sender=NOTIFICATIONS_ENRICHER_SENDER,
    template_api_client=TEMPLATES_API_SERVICE,
    email_consumer=EMAIL_CONSUMER,
)

resources = bootstrap.resolve_resources(config=config)

resources.register(application.Runner)

consumers = resources.resolve(application.Runner).consumers
