import logging
from http import HTTPStatus
from typing import Optional

from pydantic import ValidationError
from src.common.clients.email_provider_api import EmailProviderApiClient
from src.common.clients.template_api import TemplateApiClient
from src.common.exceptions import BadRequestError, ClientError, ServiceError
from src.common.repositories.notifications import NotificationsRepository
from src.workers.models.delivery import (
    DeliveryStatus,
    ReadyToSendDeliveryModel,
)
from src.workers.models.emails import EmailForSend


logger = logging.getLogger(__name__)


class EmailService:
    def __init__(
        self,
        repository: NotificationsRepository,
        template_api_client: TemplateApiClient,
        email_provider_api_client: EmailProviderApiClient,
    ):
        self._repository = repository
        self._template_api_client = template_api_client
        self._email_provider_api_client = email_provider_api_client

    async def main(self, body: bytes) -> None:
        """
        Вызывается при получении сообщения
        """
        delivery_event = self._load_model(body)

        delivery_data = await self._repository.get_delivery_for_send(
            delivery_id=delivery_event.delivery_id  # type: ignore
        )
        if not delivery_data:
            logger.warning(
                "Delivery not found: delivery_id %s",
                delivery_event.delivery_id,  # type: ignore
                exc_info=True,
            )
            return

        await self._process_email(delivery_data)

    async def _process_email(self, delivery_data: EmailForSend) -> None:
        rendered = await self.render_template(
            delivery_data.template_id, delivery_data.parameters
        )
        if not rendered:
            await self._repository.set_delivery_distribution_status(
                DeliveryStatus.FAILED,
                delivery_data.delivery_id,
                {"RenderError": "Unable to render template"},
            )
            logger.warning(
                "Template was not rendered: delivery_id %s template_id %s",
                delivery_data.delivery_id,
                delivery_data.template_id,
                exc_info=True,
            )
            return

        response = await self.send_email_to_provider(
            delivery_data.recipient.email, rendered
        )
        if not response or response.get("status_code") != HTTPStatus.OK:
            await self._repository.set_delivery_distribution_status(
                DeliveryStatus.FAILED,
                delivery_data.delivery_id,
                {"EmailProviderError": "Unable to send email to provider"},
            )
            logger.warning(
                "Error sending email to provider: delivery_id %s",
                delivery_data.delivery_id,
                exc_info=True,
            )
            return

        await self._repository.set_excluded_delivery(
            DeliveryStatus.SENT, delivery_data.delivery_id
        )
        await self._repository.set_delivery_distribution_status(
            DeliveryStatus.SENT, delivery_data.delivery_id
        )

    async def render_template(
        self, template_id: int, parameters: dict
    ) -> str | None:
        try:
            rendered = await self._template_api_client.render_template(
                template_id, parameters
            )
        except (BadRequestError, ServiceError, ClientError):
            logger.warning(
                "Rendering template caused error: template_id %s",
                template_id,
                exc_info=True,
            )
            return None
        else:
            return rendered

    async def send_email_to_provider(
        self, email: str, email_body: str
    ) -> dict | None:
        try:
            response = await self._email_provider_api_client.send_email(
                email, email_body
            )
        except (BadRequestError, ServiceError, ClientError):
            logger.warning(
                "Error sending email to provider: email %s",
                email,
                exc_info=True,
            )
            return None
        return response

    @staticmethod
    def _load_model(
        body: bytes,
    ) -> Optional[ReadyToSendDeliveryModel]:
        try:
            return ReadyToSendDeliveryModel.parse_raw(body)
        except ValidationError:
            logger.warning(
                "Fail to parse data for delivery event - %s",
                body,
                exc_info=True,
            )
        return None
