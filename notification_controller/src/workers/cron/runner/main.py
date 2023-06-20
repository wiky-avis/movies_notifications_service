from settings import DELIVERY_TRIGGER_STARTER, DeliveryTriggerStarterConfig
from settings.sender import DELIVERY_TRIGGER_STARTER_SENDER
from src.workers.cron.runner import (
    application,
    bootstrap,
)


config = DeliveryTriggerStarterConfig(
    delivery_trigger_starter=DELIVERY_TRIGGER_STARTER,
    delivery_trigger_starter_amqp_sender=DELIVERY_TRIGGER_STARTER_SENDER,
)

resources = bootstrap.resolve_resources(config=config)

resources.register(application.Runner)

daemons = resources.resolve(application.Runner).daemons
