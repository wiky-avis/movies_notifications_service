import logging

import aio_pika
from settings.daemons import BaseDaemonConfig
from src.common.base_daemon import BaseDaemon
from src.workers.cron.delivery_trigger_starter.service import (
    DeliveryTriggerStarterService,
)


logger = logging.getLogger(__name__)


class DeliveryTriggerStarter(BaseDaemon):
    def __init__(
        self,
        config: BaseDaemonConfig,
        service: DeliveryTriggerStarterService,
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
