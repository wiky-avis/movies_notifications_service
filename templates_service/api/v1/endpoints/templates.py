from http import HTTPStatus
from typing import Any, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from fastapi.responses import JSONResponse

from templates_service.common.models.inputs import CreateTemplateIn
from templates_service.common.models.responses import (
    CreateTemplateOut,
    HTTPErrorResponse,
)

# from templates_service.common.models.templates import NotificationTemplate
from templates_service.common.services.templates import TemplatesService
from templates_service.containers import Container
from templates_service.settings import settings


router = APIRouter()


@router.post(
    "/templates",
    summary="Создать новый шаблон для коммуникации",
    description="Создает новый шаблон и возвращает статус",
    response_model=CreateTemplateOut,
    responses={
        409: {
            "model": HTTPErrorResponse,
            "description": "Если такой шаблон уже существует",
        },
        500: {
            "model": HTTPErrorResponse,
            "description": "Внутренняя ошибка сервиса",
        },
    },
)
@inject
async def create_template(
    token_header: Optional[str] = Header(
        None, alias=settings.auth.token_header
    ),
    body: CreateTemplateIn = Body(...),
    templates_service: TemplatesService = Depends(
        Provide[Container.notifications_service]
    ),
) -> Any:
    """
    Принимает полное описание шаблона, валидирует его и создает.
    Запись в базу происходит только при успешной валидации.
    Если шаблон уже существует, то вернуть ошибку.

    На вход ожидаются следующие параметры:
    - template_id - str - уникальное название шаблона
    - template_body - str - HTML шаблон с параметрами
    - description - описание
    - channel - канал
    - type - тип отправки

    Возвращает статус создания шаблона.
    """
    if not token_header:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Token required")
    if token_header not in settings.auth.tokens:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Forbidden")

    return await templates_service.create_template(body)


@router.patch(
    "/templates",
    summary="Изменение существующего шаблона",
    description="Изменяет существующий шаблон с помощью привденных параметров",
)
async def update_template() -> JSONResponse:
    """
    Принимает id уже существующего шаблона те параметры, которые в нем нужно поменять.
    Он берет шаблон из базы, вносит нужные изменения, снова пытается его провалидировать.
    Если все ок, то обновляет запись в базе.
    Нужно лочить шаблон для изменения во время таких вещей.

    На вход ожидаются следующие параметры:
    - template_id - str - уникальное название шаблона
    - template_body - str - HTML шаблон с параметрами
    - Еще какие-то параметры, которые нужно поменять

    Возвращает статус изменения шаблона.
    """
    return JSONResponse("ok")


@router.delete(
    "/templates",
    summary="Удаление существующего шаблона",
    description="Удаляет шаблон из базы",
)
async def delete_template() -> JSONResponse:
    """
    Принимает id уже существующего шаблона.
    Если такого шаблона нет, возвращаем ошибку.

    На вход ожидаются следующие параметры:
    - template_id - str - уникальное название шаблона

    Возвращает статус удаления шаблона.
    """
    return JSONResponse("ok")


@router.get(
    "/templates",
    summary="Удаление существующего шаблона",
    description="Удаляет шаблон из базы",
)
async def get_template() -> JSONResponse:
    """
    Принимает id уже существующего шаблона.
    Если такого шаблона нет, возвращаем ошибку.

    На вход ожидаются следующие параметры в URL:
    - template_id - str - выдаст определенный шаблон
    - search_mode - str - Тип поиска. match или contains. Полное соответствие и содержит соответственно.
    - channels - list - какие каналы нужны

    Возвращает шаблоны, которые подходят под заданные параметры.
    """
    return JSONResponse("ok")


@router.get(
    "/templates/render",
    summary="Рендерит заполненный шаблон",
    description="Заполняет шаблон предоставленными параметрами и рендерит шаблон",
)
async def render_template() -> JSONResponse:
    """
    Принимает id уже существующего шаблона.
    Если такого шаблона нет, возвращаем ошибку.
    Также получаем все параметры для подстановки.
    Если параметр отсутствует, но есть дефолтное значение, то будет использовано оно.
    Если параметр обязательный, то возвращаем ошибку.

    На вход ожидаются следующие параметры в URL:
    - template_id - str - выдаст определенный шаблон
    - parameters - dict - поставляемые параметры

    Возвращает срендеренный HTML шаблон
    """
    return JSONResponse("ok")
