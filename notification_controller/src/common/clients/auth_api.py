import dpath
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
    def default_headers(self) -> dict:
        return {"X-Token": self.token}

    async def get_user_by_id(self, user_id: str) -> dict:
        """Получить данные пользователя."""

        url = "/api/srv/users"
        params = {"user_id": user_id}
        response_body = await self.get(
            url=url, headers=self.default_headers, params=params
        )
        # response = response_body.json()
        # TODO: удалить
        response = {
            "success": True,
            "error": None,
            "result": {
                "id": "73c9c344-5230-478d-95bf-b100f8569440",
                "email": "123@123.ru",
                "roles": ["ROLE_PORTAL_USER"],
                "verified_mail": True,
                "registered_on": "2023-06-20 07:13:22",
                "tz": "-8",
            },
        }
        return dpath.get(response, "result", default=None)  # type: ignore


def resolve_auth_api_client(config: AuthApiSettings):
    return AuthApiClient(
        base_url=config.url,
        token=config.token,
    )
