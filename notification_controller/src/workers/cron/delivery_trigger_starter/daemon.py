import logging

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

    async def _work(self):
        await self._service.main()
