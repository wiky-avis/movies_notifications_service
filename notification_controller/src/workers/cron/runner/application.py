import logging

import aiomisc
from src.common.base_daemon import BaseDaemonRunner
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.connectors.db import DbConnector
from src.workers.cron.delivery_trigger_starter.daemon import (
    DeliveryTriggerStarter,
)


logger = logging.getLogger(__name__)


class Runner(BaseDaemonRunner):
    def __init__(
        self,
        db: DbConnector,
        delivery_trigger_starter: DeliveryTriggerStarter,
        amqp_sender: AMQPSenderPikaConnector,
    ):
        self._db = db
        self._delivery_trigger_starter = delivery_trigger_starter
        self._amqp_sender = amqp_sender

    @property
    def daemons(self):
        self._setup()
        return self._resolve_daemon_list()

    @property
    def clients(self):
        return self._resolve_client_list()

    def _setup(self):
        @aiomisc.receiver(aiomisc.entrypoint.PRE_START)
        async def startup(entrypoint, services):
            await self._amqp_sender.setup()
            await self._db.connect()

            for daemon in self.daemons:
                await daemon.startup()

            logger.info("Server started")

        @aiomisc.receiver(aiomisc.entrypoint.POST_STOP)
        async def shutdown(entrypoint):
            await self._amqp_sender.close()
            await self._db.disconnect()

            for daemon in self.daemons:
                await daemon.shutdown()

            for client in self.clients:
                await client.close()
