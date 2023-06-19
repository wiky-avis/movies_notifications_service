import logging

from src.common.clients.auth_api import AuthApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.repositories.notifications import NotificationsRepository


logger = logging.getLogger(__name__)


class NotificationsEnricherService:
    def __init__(
        self,
        repository: NotificationsRepository,
        auth_api_client: AuthApiClient,
        amqp_sender: AMQPSenderPikaConnector,
    ):
        self._repository = repository
        self._auth_api_client = auth_api_client
        self._amqp_sender = amqp_sender

    async def main(self, body: bytes):
        pass
