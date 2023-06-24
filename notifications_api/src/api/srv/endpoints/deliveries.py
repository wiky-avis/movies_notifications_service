from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from src.api.models.delivery import DeliveryModel
from src.common.responses import ApiResponse, wrap_response
from src.common.services.notifications import NotificationsService
from src.containers import Container
from src.settings import token_settings
from src.settings.token import NOTIFICATIONS_SRV_TOKENS
from starlette import status


router = APIRouter()


@router.post(
    "/v1/deliveries",
    summary="Регистрация отправки коммуникации",
    description="Принимает на вход модель отправки, генерирует delivery_id и пишет его в очередь",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def create_delivery(
    token_header: str | None = Header(None, alias=token_settings.token_header),
    body: DeliveryModel = Body(...),
    notifications_service: NotificationsService = Depends(
        Provide[Container.notifications_service]
    ),
):
    """
    Входной компонент системы. Принимает сообщения для отправки и регистрирует их в очереди.
    Производит минимальную валидацию и возвращает сгенерированный delivery_id.
    Основные пользователи:
    - Админка - разовые отправки инициированные из интерфейса
    - Внутренние сервисы - регулярные или триггерные отправки.
      Логика сбора данных настраивается внутри сервисов и в нужный момент они сами дергают апишку
    """
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in NOTIFICATIONS_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await notifications_service.create_delivery(body)


@router.get(
    "/v1/deliveries/{delivery_id}",
    summary="Получение статуса отправки",
    description="По переданному id отправки возвращает ее текущий статус",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def get_delivery(
    delivery_id: int,
    token_header: str | None = Header(None, alias=token_settings.token_header),
    notifications_service: NotificationsService = Depends(
        Provide[Container.notifications_service]
    ),
):
    """
    Ходит в БД в специальную таблицу со статусами и возвращает все имеющуюся информацию по переданному id отправки.
    """
    if not token_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token required")
    if token_header not in NOTIFICATIONS_SRV_TOKENS:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    return await notifications_service.get_delivery_by_id(delivery_id)
