import logging
from http import HTTPStatus

from httpx import AsyncClient
from settings.services import EmailProviderApiSettings


logger = logging.getLogger(__name__)


class EmailProviderApiClient(AsyncClient):
    def __init__(
        self,
        base_url: str,
        token: str,
    ):
        super().__init__(base_url=base_url)
        self.token = token

    @property
    def default_headers(self) -> dict:
        return {"X-Token": self.token}

    async def send_email(self, email: str, email_body: str) -> dict:
        """Получить данные пользователя."""

        params = {"email": email, "email_body": email_body}
        logger.info("Email sent", params)
        return {"status_code": HTTPStatus.OK}

    async def _send_email(self, email: str, email_body: str) -> dict:
        """Получить данные пользователя."""

        url = "/send_email"
        params = {"email": email, "email_body": email_body}
        response = await self.get(  # type: ignore
            url=url, headers=self.default_headers, params=params
        )
        status_code = response.status_code
        response_body = response.json()
        response_body["status_code"] = status_code
        return response_body


def resolve_template_api_client(config: EmailProviderApiSettings):
    return EmailProviderApiClient(
        base_url=config.url,
        token=config.token,
    )
