from httpx import AsyncClient
from settings.services import TemplateApiSettings


class TemplateApiClient(AsyncClient):
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

    async def render_template(
        self, template_id: int, parameters: dict
    ) -> str | None:
        """Получить данные пользователя."""

        url = "/templates/render"
        params = {"template_id": template_id, "parameters": parameters}
        response_body = await self.get(
            url=url, headers=self.default_headers, params=params  # type: ignore
        )
        response = response_body.json()
        rendered = response.get("rendered")
        if rendered:
            rendered = str(rendered)
        return rendered


def resolve_template_api_client(config: TemplateApiSettings):
    return TemplateApiClient(
        base_url=config.url,
        token=config.token,
    )
