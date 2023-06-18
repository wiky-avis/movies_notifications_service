import logging

import aio_pika
from settings.consumers import BaseConsumerSettings
from src.common.base_consumer import BaseConsumer
from src.workers.consumers.notifications_enricher_consumer.service import (
    NotificationsEnricherService,
)


logger = logging.getLogger(__name__)


class NotificationsEnricherConsumer(BaseConsumer):
    def __init__(
        self,
        config: BaseConsumerSettings,
        service: NotificationsEnricherService,
    ):
        super().__init__(config=config)
        self._config = config
        self._service = service

    async def _process_message(
        self, message: aio_pika.abc.AbstractIncomingMessage
    ):
        async with message.process():
            await self._service.main(body=message.body)

    async def _make_queue_bindings(self):
        await self._queue.bind(
            exchange=self._config.exchange_name,
            routing_key=self._config.routing_key,
        )
