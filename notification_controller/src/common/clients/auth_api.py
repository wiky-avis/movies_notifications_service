from typing import Dict

from httpx import AsyncClient
from settings.services import AuthApiSettings


class AuthApiClient(AsyncClient):
    def __init__(
        self,
        base_url: str,
        token: str,
    ):
        super().__init__(base_url=base_url)
        self.token = token

    @property
    def default_headers(self) -> Dict:
        return {"X-Token": self.token}

    async def get_user_by_id(self, user_id: str):
        """Получить данные пользователя."""

        # url = f"/api/srv/users/{user_id}"
        # response_body = await self.get(url=url, headers=self.default_headers)
        # resp = response_body.json()
        # return resp


def resolve_auth_api_client(config: AuthApiSettings):
    return AuthApiClient(
        base_url=config.url,
        token=config.token,
    )
