import punq
from settings.daemons import DeliveryTriggerStarterConfig
from src.common.connectors.amqp import (
    AMQPSenderPikaConnector,
    resolve_amqp_sender_client,
)
from src.common.connectors.db import DbConnector
from src.common.repositories.notifications import NotificationsRepository
from src.workers.cron.delivery_trigger_starter.daemon import (
    DeliveryTriggerStarter,
)
from src.workers.cron.delivery_trigger_starter.service import (
    DeliveryTriggerStarterService,
)


def resolve_resources(config: DeliveryTriggerStarterConfig) -> punq.Container:
    container = punq.Container()

    container.register(service=DbConnector)
    container.register(
        service=AMQPSenderPikaConnector,
        instance=resolve_amqp_sender_client(
            config=config.delivery_trigger_starter_amqp_sender
        ),
    )
    container.register(service=NotificationsRepository)
    container.register(service=DeliveryTriggerStarterService)
    container.register(
        service=DeliveryTriggerStarter,
        factory=DeliveryTriggerStarter,
        config=config.delivery_trigger_starter,
    )
    return container
