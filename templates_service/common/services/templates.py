from http import HTTPStatus

from fastapi import HTTPException

from templates_service.common.exceptions import (
    DatabaseError,
    TemplateValidationError,
)
from templates_service.common.models.inputs import CreateTemplateIn
from templates_service.common.models.responses import CreateTemplateOut
from templates_service.common.repositories.templates import TemplatesRepository


class TemplatesService:
    def __init__(self, repository: TemplatesRepository):
        self._repository = repository

    async def create_template(self, template_input: CreateTemplateIn):
        # Примерно так можно обозначить стандартные переменные
        # {{ my_variable|default('my_variable is not defined') }}
        try:
            # Проверяем корректность шаблона. Выдаст ошибку, есть что-то не понравится
            template = self._repository.parse_html(template_input)

            template_id = await self._repository.check_template(
                template.template_name
            )

            if template_id:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail="Данный шаблон уже существует. В можете его изменить через другой запрос.",
                )

            await self._repository.create_template(template)

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

        return CreateTemplateOut(status="Шаблон создан")
