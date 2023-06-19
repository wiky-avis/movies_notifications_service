from http import HTTPStatus
from typing import Any, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Header, HTTPException

from templates_service.common.models.inputs import (
    CreateTemplateIn,
    GetTemplateIn,
    RenderTemplateIn,
    UpdateTemplateIn,
)
from templates_service.common.models.responses import (
    HTTPErrorResponse,
    RenderTemplateOut,
    TemplateOut,
    TemplatesListing,
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
    response_model=TemplateOut,
    responses={
        400: {
            "model": HTTPErrorResponse,
            "description": "Ошибка валидации шаблона",
        },
        401: {
            "model": HTTPErrorResponse,
            "description": "Не подписан сервисным токеном",
        },
        403: {
            "model": HTTPErrorResponse,
            "description": "Предоставленный токен не списке разрешенных",
        },
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
    - template_name - str - уникальное название шаблона
    - template_body - str - HTML шаблон с параметрами
    - description - описание
    - channel - канал
    - type - тип отправки

    Возвращает статус создания шаблона и его id.
    """
    if not token_header:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Token required")
    if token_header not in settings.auth.tokens:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Forbidden")

    return await templates_service.create_template(body)


@router.patch(
    "/templates",
    summary="Изменение существующего шаблона",
    description="Изменяет существующий шаблон с помощью привeденных параметров",
    response_model=TemplateOut,
    responses={
        400: {
            "model": HTTPErrorResponse,
            "description": "Ошибка валидации шаблона",
        },
        401: {
            "model": HTTPErrorResponse,
            "description": "Не подписан сервисным токеном",
        },
        403: {
            "model": HTTPErrorResponse,
            "description": "Предоставленный токен не списке разрешенных",
        },
        500: {
            "model": HTTPErrorResponse,
            "description": "Внутренняя ошибка сервиса",
        },
    },
)
async def update_template(
    token_header: Optional[str] = Header(
        None, alias=settings.auth.token_header
    ),
    body: UpdateTemplateIn = Body(...),
    templates_service: TemplatesService = Depends(
        Provide[Container.notifications_service]
    ),
) -> Any:
    """
    Принимает id уже существующего шаблона те параметры, которые в нем нужно поменять.
    Он берет шаблон из базы, вносит нужные изменения, снова пытается его провалидировать.
    Если все ок, то обновляет запись в базе.

    На вход ожидаются следующие параметры:
    - template_id - int - уникальное id шаблона

    Опционально:
    - template_name - Уникальное название шаблона
    - template_body - HTML шаблон с параметрами
    - description - описание
    - channel - канал
    - type - тип отправки

    Возвращает статус изменения шаблона.
    """
    if not token_header:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Token required")
    if token_header not in settings.auth.tokens:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Forbidden")

    return await templates_service.update_template(body)


@router.delete(
    "/templates{template_id}",
    summary="Удаление существующего шаблона",
    description="Удаляет шаблон из базы",
    response_model=TemplateOut,
    responses={
        401: {
            "model": HTTPErrorResponse,
            "description": "Не подписан сервисным токеном",
        },
        403: {
            "model": HTTPErrorResponse,
            "description": "Предоставленный токен не списке разрешенных",
        },
        500: {
            "model": HTTPErrorResponse,
            "description": "Внутренняя ошибка сервиса",
        },
    },
)
async def delete_template(
    template_id: int,
    token_header: Optional[str] = Header(
        None, alias=settings.auth.token_header
    ),
    templates_service: TemplatesService = Depends(
        Provide[Container.notifications_service]
    ),
) -> Any:
    """
    Принимает id уже существующего шаблона.

    На вход ожидаются следующие параметры:
    - template_id - str - уникальное название шаблона

    Возвращает статус удаления шаблона.
    """
    if not token_header:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Token required")
    if token_header not in settings.auth.tokens:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Forbidden")

    return await templates_service.delete_template(template_id)


@router.get(
    "/templates",
    summary="Удаление существующего шаблона",
    description="Удаляет шаблон из базы",
    response_model=TemplatesListing,
    responses={
        401: {
            "model": HTTPErrorResponse,
            "description": "Не подписан сервисным токеном",
        },
        403: {
            "model": HTTPErrorResponse,
            "description": "Предоставленный токен не списке разрешенных",
        },
        500: {
            "model": HTTPErrorResponse,
            "description": "Внутренняя ошибка сервиса",
        },
    },
)
async def get_template(
    token_header: Optional[str] = Header(
        None, alias=settings.auth.token_header
    ),
    body: GetTemplateIn = Body(...),
    templates_service: TemplatesService = Depends(
        Provide[Container.notifications_service]
    ),
) -> Any:
    """
    Ищет шаблоны по запросу.

    На вход ожидаются следующие параметры в URL:
    - search_field - str - По какому полю искать
    - search_query - str - Значение поиска
    - search_mode - str - Тип поиска

    Возвращает шаблоны, которые подходят под заданные параметры.
    """
    if not token_header:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Token required")
    if token_header not in settings.auth.tokens:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Forbidden")

    return await templates_service.search_templates(body)


@router.get(
    "/templates/render",
    summary="Рендерит заполненный шаблон",
    description="Заполняет шаблон предоставленными параметрами и рендерит шаблон",
    response_model=RenderTemplateOut,
    responses={
        400: {
            "model": HTTPErrorResponse,
            "description": "Ошибка валидации шаблона",
        },
        401: {
            "model": HTTPErrorResponse,
            "description": "Не подписан сервисным токеном",
        },
        403: {
            "model": HTTPErrorResponse,
            "description": "Предоставленный токен не списке разрешенных",
        },
        404: {
            "model": HTTPErrorResponse,
            "description": "Шаблон не найден",
        },
        500: {
            "model": HTTPErrorResponse,
            "description": "Внутренняя ошибка сервиса",
        },
    },
)
async def render_template(
    token_header: Optional[str] = Header(
        None, alias=settings.auth.token_header
    ),
    body: RenderTemplateIn = Body(...),
    templates_service: TemplatesService = Depends(
        Provide[Container.notifications_service]
    ),
) -> Any:
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
    if not token_header:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Token required")
    if token_header not in settings.auth.tokens:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Forbidden")

    return await templates_service.render_template(body)
