from http import HTTPStatus
from unittest import mock

from src.api.models.subscription import ChannelType
from src.common.repositories.notifications import NotificationsRepository
from tests.vars.users import mock_unsubscribe_user


async def test_create_delivery_ok(test_client, test_app):
    body = {
        "user_id": "f51f3683-7758-402e-9cf4-785f840d8738",
        "channel_type": ChannelType.EMAIL.value,
    }
    user_subscription_service_mock = mock.AsyncMock(
        spec=NotificationsRepository
    )
    user_subscription_service_mock.unsubscribe_user.return_value = (
        mock_unsubscribe_user()
    )
    with test_app.container.user_subscription_service.override(
        user_subscription_service_mock
    ):
        response = await test_client.post(
            "/api/v1/users/unsubscribe", json=body
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "success": True,
        "result": "Ok",
        "errors": None,
    }
