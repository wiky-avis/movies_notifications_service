import abc
import logging

import aiocron
import aiomisc
from httpx import AsyncClient
from settings.daemons import BaseDaemonConfig


logger = logging.getLogger(__name__)


class BaseDaemon(aiomisc.Service):
    def __init__(self, config: BaseDaemonConfig):
        super().__init__()
        self._config = config

    @property
    def _job(self):
        return aiocron.crontab(
            self._config.cron,
            func=self._work,
            start=False,
        )

    @property
    def daemon(self):
        if not self._config.run:
            return None
        return self

    async def start(self):
        logger.info("%s service start.", self.__class__.__name__)

    async def stop(self, exception: Exception = None):  # type: ignore
        logger.info("%s service stop.", self.__class__.__name__)

    async def startup(self):
        if self.daemon is None:
            return
        self._job.start()
        logger.info("%s connection is established.", self.__class__.__name__)

    async def shutdown(self):
        if self.daemon is None:
            return
        self._job.stop()
        logger.info("%s connection is closed.", self.__class__.__name__)

    @abc.abstractmethod
    async def _work(self):
        raise NotImplementedError


class BaseDaemonRunner:
    def _resolve_daemon_list(self) -> list[BaseDaemon]:
        return [
            value
            for value in self.__dict__.values()
            if isinstance(value, BaseDaemon) and value.daemon is not None
        ]

    def _resolve_client_list(self) -> list[AsyncClient]:
        return [
            value
            for value in self.__dict__.values()
            if isinstance(value, AsyncClient)
        ]
