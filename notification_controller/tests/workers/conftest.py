import re
from http import HTTPStatus

import punq
import pytest
import respx
from src.common.clients.auth_api import AuthApiClient
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.common.connectors.db import DbConnector
from src.common.repositories.notifications import NotificationsRepository
from src.workers.consumers.notifications_enricher_consumer.service import (
    NotificationsEnricherService,
)


@pytest.fixture
async def resolve_amqp_sender_connector():
    return AMQPSenderPikaConnector(config={})


@pytest.fixture
async def test_database():
    db = DbConnector()
    await db.connect()

    yield db

    await db.disconnect()


@pytest.fixture
async def test_auth_api_client():
    client = AuthApiClient(base_url="http://0.0.0.0/", token="test")
    yield client


@pytest.fixture
def notifications_enricher_service(
    test_database, test_auth_api_client
) -> NotificationsEnricherService:
    container = punq.Container()

    container.register(service=DbConnector, instance=test_database)

    container.register(
        service=AuthApiClient,
        instance=test_auth_api_client,
    )
    container.register(
        service=AMQPSenderPikaConnector, instance=resolve_amqp_sender_connector
    )

    container.register(service=NotificationsRepository)
    container.register(service=NotificationsEnricherService)

    yield container.resolve(NotificationsEnricherService)


@pytest.fixture
def mock_external_services():
    with respx.mock(base_url="http://0.0.0.0/") as respx_mock:
        yield respx_mock


@pytest.fixture
async def mock_auth_api_ok(mock_external_services):
    resp = {
        "success": True,
        "error": None,
        "result": {
            "id": "73c9c344-5230-478d-95bf-b100f8569440",
            "email": "123@123.ru",
            "roles": ["ROLE_PORTAL_USER"],
            "verified_mail": True,
            "registered_on": "2023-06-20 07:13:22",
            "tz": "-8",
        },
    }
    mock_external_services.get(re.compile(".*/api/srv/users.*")).respond(
        json=resp,
        status_code=HTTPStatus.OK,
    )
