from http import HTTPStatus
from unittest import mock

from src.common.repositories.notifications import NotificationsRepository
from tests.vars.delivery import (
    get_deliveries_response,
    mock_create_delivery,
    mock_get_delivery_by_id,
)


async def test_create_delivery_ok(test_client, test_app):
    body = {
        "template_id": 1,
        "recipient": {
            "user_id": "f51f3683-7758-402e-9cf4-785f840d8738",
            "email": "test@ya.ru",
        },
        "parameters": [
            {"name": "subject", "value": "Приветственное письмо"},
            {"name": "username", "value": "vasya"},
            {"name": "age", "value": "60"},
        ],
        "channel": "email",
        "type": "not_night",
        "sender": "ugs_service",
    }
    test_client.headers["X-AUTH-TOKEN"] = "test"
    notifications_service_mock = mock.AsyncMock(spec=NotificationsRepository)
    notifications_service_mock.create_delivery.return_value = (
        mock_create_delivery()
    )
    with test_app.container.notifications_service.override(
        notifications_service_mock
    ):
        response = await test_client.post("/api/srv/v1/deliveries", json=body)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == get_deliveries_response()


async def test_get_delivery_by_id_ok(test_client, test_app):
    delivery_id = 1

    test_client.headers["X-AUTH-TOKEN"] = "test"
    notifications_service_mock = mock.AsyncMock(spec=NotificationsRepository)
    notifications_service_mock.get_delivery_by_id.return_value = (
        mock_get_delivery_by_id()
    )
    with test_app.container.notifications_service.override(
        notifications_service_mock
    ):
        response = await test_client.get(
            f"/api/srv/v1/deliveries/{delivery_id}"
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == get_deliveries_response()
