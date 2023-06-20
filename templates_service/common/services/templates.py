import json
from http import HTTPStatus

from fastapi import HTTPException

from templates_service.common.exceptions import (
    DatabaseError,
    TemplateValidationError,
)
from templates_service.common.models.inputs import (
    CreateTemplateIn,
    GetTemplateIn,
    RenderTemplateIn,
    UpdateTemplateIn,
)
from templates_service.common.models.responses import (
    RenderTemplateOut,
    TemplateOut,
    TemplatesListing,
)
from templates_service.common.models.templates import NotificationTemplate
from templates_service.common.repositories.templates import TemplatesRepository


class TemplatesService:
    def __init__(self, repository: TemplatesRepository):
        self._repository = repository

    async def create_template(self, template_input: CreateTemplateIn):
        # Примерно так можно обозначить стандартные переменные
        # {{ my_variable|default('my_variable is not defined') }}
        try:
            # Проверяем корректность шаблона. Выдаст ошибку, есть что-то не понравится
            (
                mandatory_parameters,
                optional_parameters,
            ) = self._repository.parse_html(template_input.template_body)

            template = NotificationTemplate(
                template_name=template_input.template_name,
                template_body=template_input.template_body,
                description=template_input.description,
                mandatory_parameters=mandatory_parameters,
                optional_parameters=optional_parameters,
                channel=template_input.channel,
                type=template_input.type_,
            )

            template_exists = await self._repository.check_template(
                template.template_name
            )

            if template_exists:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail="Данный шаблон уже существует. Вы можете его изменить через другой запрос.",
                )

            template_id = await self._repository.create_template(template)

            return TemplateOut(status="Шаблон создан", template_id=template_id)

        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create a new delivery.",
            )
        except TemplateValidationError as ex:
            if hasattr(ex, "message"):
                error_message = ex.message
            else:
                error_message = "Ошибка валидации шаблона"

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=error_message,
            )

    async def update_template(
        self, template_input: UpdateTemplateIn
    ) -> TemplateOut:
        update_fields = template_input.dict(
            exclude={"template_id"}, exclude_none=True
        )

        if not update_fields:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="No fields to change",
            )

        if "template_body" in update_fields:
            (
                mandatory_parameters,
                optional_parameters,
            ) = self._repository.parse_html(template_input.template_body)
            update_fields["mandatory_parameters"] = json.dumps(
                mandatory_parameters
            )
            update_fields["optional_parameters"] = json.dumps(
                optional_parameters
            )

        try:
            await self._repository.update_template(
                template_input.template_id, update_fields
            )

            return TemplateOut(
                status="Шаблон обновлен",
                template_id=template_input.template_id,
            )

        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create a new delivery.",
            )
        except TemplateValidationError as ex:
            if hasattr(ex, "message"):
                error_message = ex.message
            else:
                error_message = "Ошибка валидации шаблона"

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=error_message,
            )

    async def delete_template(self, template_id: int) -> TemplateOut:
        try:
            await self._repository.delete_template(template_id)

            return TemplateOut(status="Шаблон удален", template_id=template_id)

        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create a new delivery.",
            )

    async def search_templates(
        self, search_model: GetTemplateIn
    ) -> TemplatesListing:
        try:
            if search_model.search_mode.EQUALS:
                result = await self._repository.find_equals(
                    search_model.search_field, search_model.search_query
                )
            elif search_model.search_mode.ALL:
                result = await self._repository.get_all_templates()
            else:
                result = await self._repository.find_matches(
                    search_model.search_field, search_model.search_query
                )

            if result:
                return TemplatesListing(
                    status="Результаты поиска",
                    count=len(result),
                    items=result,
                )
            else:
                return TemplatesListing(
                    status="Шаблоны не найдены",
                    count=0,
                    items=[],
                )

        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create a new delivery.",
            )

    async def render_template(
        self, template_input: RenderTemplateIn
    ) -> RenderTemplateOut:
        try:
            result = await self._repository.find_equals(
                "template_id", template_input.template_id
            )
            if not result:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="No template with provided id exists",
                )

            template = result[0]

            if template.mandatory_parameters:
                for key in template.mandatory_parameters:
                    if key not in template_input.parameters:
                        raise HTTPException(
                            status_code=HTTPStatus.BAD_REQUEST,
                            detail="Mandatory parameter not provided - " + key,
                        )

            rendered = self._repository.render(
                template.template_body, template_input.parameters
            )

            return RenderTemplateOut(rendered=rendered)

        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create a new delivery.",
            )
        except TemplateValidationError as ex:
            if hasattr(ex, "message"):
                error_message = ex.message
            else:
                error_message = "Ошибка валидации шаблона"

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=error_message,
            )
