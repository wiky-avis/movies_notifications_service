import logging
from typing import Any

from templates_service.common.connectors.db import DbConnector
from templates_service.common.exceptions import DatabaseError

# from templates_service.common.models.inputs import CreateTemplateIn
from templates_service.common.models.templates import NotificationTemplate
from templates_service.common.repositories import queries
from templates_service.common.validators.validator import HTMLValidator


logger = logging.getLogger(__name__)


class TemplatesRepository:
    def __init__(self, db: DbConnector, html_validator: HTMLValidator):
        self._db = db
        self.html_validator = html_validator

    def parse_html(self, template_input) -> NotificationTemplate:
        return self.html_validator.parse(template_input)

    async def check_template(self, template_name: str) -> Any:
        """
        Проверяет есть ли такой шаблон в базе

        Параметры:
        - template_name - Название

        Ответ:
        - True - если он есть
        - False - если нет
        """
        try:
            result = await self._db.pool.fetchval(  # type: ignore[union-attr]
                queries.CHECK_TEMPLATE,
                template_name,
            )
        except Exception:
            logger.exception(
                "Failed to search for template: template_name %s",
                template_name,
                exc_info=True,
            )
            raise DatabaseError()
        else:
            return result

    async def create_template(self, template: NotificationTemplate) -> None:
        try:
            await self._db.pool.execute(  # type: ignore[union-attr]
                queries.CREATE_TEMPLATE,
                template.template_name,
                template.template_body,
                template.description,
                template.mandatory_parameters,
                template.optional_parameters,
                template.channel,
                template.type_,
            )
        except Exception:
            logger.exception(
                "Failed to create new template: template_name %s",
                template.template_name,
                exc_info=True,
            )
            raise DatabaseError()
