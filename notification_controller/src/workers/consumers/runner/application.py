import logging

import aiomisc
from src.common.base_consumer import BaseRunner
from src.common.clients.auth_api import AuthApiClient
from src.common.connectors.db import DbConnector
from src.workers.consumers.notifications_enricher_consumer.service import (
    NotificationsEnricherService,
)


logger = logging.getLogger(__name__)


class Runner(BaseRunner):
    def __init__(
        self,
        db: DbConnector,
        auth_api_client: AuthApiClient,
        notifications_enricher_consumer: NotificationsEnricherService,
    ):
        self._db = db
        self._auth_api_client = auth_api_client
        self._notifications_enricher_consumer = notifications_enricher_consumer

    @property
    def consumers(self):
        self._setup()
        return self._resolve_consumer_list()

    @property
    def clients(self):
        return self._resolve_client_list()

    def _setup(self):
        @aiomisc.receiver(aiomisc.entrypoint.PRE_START)
        async def startup(entrypoint, services):
            await self._db.connect()

            for consumer in self.consumers:
                await consumer.startup()

            logger.info("Server started")

        @aiomisc.receiver(aiomisc.entrypoint.POST_STOP)
        async def shutdown(entrypoint):
            await self._db.disconnect()

            for consumer in self.consumers:
                await consumer.shutdown()

            for client in self.clients:
                await client.close()
