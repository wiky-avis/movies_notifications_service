import logging
from typing import Any

from pydantic import parse_obj_as

from templates_service.common.connectors.db import DbConnector
from templates_service.common.exceptions import DatabaseError
from templates_service.common.models.inputs import SearchField
from templates_service.common.models.templates import NotificationTemplate
from templates_service.common.repositories import queries
from templates_service.common.validators.validator import HTMLValidator


logger = logging.getLogger(__name__)


class TemplatesRepository:
    def __init__(self, db: DbConnector, html_validator: HTMLValidator):
        self._db = db
        self.html_validator = html_validator

    def parse_html(self, template_input) -> tuple[list | None, dict | None]:
        return self.html_validator.parse(template_input)

    def render(self, template_body: str, template_parameters: dict) -> str:
        return self.html_validator.render(template_body, template_parameters)

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

    async def create_template(self, template: NotificationTemplate) -> int:
        try:
            template_id = await self._db.pool.fetchval(  # type: ignore[union-attr]
                queries.CREATE_TEMPLATE,
                template.template_name,
                template.template_body,
                template.description,
                template.mandatory_parameters,
                template.optional_parameters,
                template.channel,
                template.type_,
            )
            return int(template_id)
        except Exception:
            logger.exception(
                "Failed to create new template: template_name %s",
                template.template_name,
                exc_info=True,
            )
            raise DatabaseError()

    async def update_template(
        self, template_id: int, update_fields: dict
    ) -> None:
        try:
            update_template_query = queries.UPDATE_TEMPLATE_START

            for key, value in update_fields.items():
                update_field = key + " = " + str(value) + ", \n"
                update_template_query += update_field

            template_id_filter = (
                "where template_id = " + str(template_id) + ";"
            )
            update_template_query += template_id_filter

            await self._db.pool.execute(update_template_query)  # type: ignore[union-attr]

        except Exception:
            logger.exception(
                "Failed to delete template: template_id %s",
                template_id,
                exc_info=True,
            )
            raise DatabaseError()

    async def delete_template(self, template_id: int) -> None:
        try:
            await self._db.pool.execute(  # type: ignore[union-attr]
                queries.DELETE_TEMPLATE, template_id
            )
        except Exception:
            logger.exception(
                "Failed to delete template: template_id %s",
                template_id,
                exc_info=True,
            )
            raise DatabaseError()

    async def find_equals(
        self, search_field: str, search_value: str | int
    ) -> list[NotificationTemplate]:
        try:
            rows = await self._db.pool.fetch(  # type: ignore[union-attr]
                queries.EQUALS_SEARCH,
                search_field,
                search_value,
            )

            if not rows:
                return []

            templates = [dict(row) for row in rows]

            return parse_obj_as(list[NotificationTemplate], templates)

        except Exception:
            logger.exception(
                "Failed to find templates: search_field %s, search_value %s",
                search_field,
                search_value,
                exc_info=True,
            )
            raise DatabaseError()

    async def find_matches(
        self, search_field: str, search_value: str | int
    ) -> list[NotificationTemplate]:
        if search_field == SearchField.TEMPLATE_ID:
            return await self.find_equals(search_field, search_value)

        try:
            rows = await self._db.pool.fetch(  # type: ignore[union-attr]
                queries.MATCH_SEARCH,
                search_field,
                str(search_value),
            )

            if not rows:
                return []

            templates = [dict(row) for row in rows]

            return parse_obj_as(list[NotificationTemplate], templates)

        except Exception:
            logger.exception(
                "Failed to find templates: search_field %s, search_value %s",
                search_field,
                search_value,
                exc_info=True,
            )
            raise DatabaseError()

    async def get_all_templates(self) -> list[NotificationTemplate]:
        try:
            rows = await self._db.pool.fetch(queries.ALL_SEARCH)  # type: ignore[union-attr]

            if not rows:
                return []

            templates = [dict(row) for row in rows]

            return parse_obj_as(list[NotificationTemplate], templates)

        except Exception:
            logger.exception(
                "Failed to find templates",
                exc_info=True,
            )
            raise DatabaseError()
