import json
from unittest.mock import AsyncMock

import pytest
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.workers.models.delivery import (
    DeliveryChannel,
    DeliveryStatus,
    DeliveryType,
    EventType,
)
from tests.vars.tables import NOTIFICATIONS_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [NOTIFICATIONS_TABLES], indirect=True)
async def test_notifications_enricher_consumer_ok(
    test_database,
    monkeypatch,
    notifications_enricher_service,
    mock_auth_api_ok,
):
    delivery_id = await test_database.pool.fetchval(
        """INSERT INTO deliveries(template_id, recipient, parameters, channel, "type", sender)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING delivery_id;
            """,
        123,
        {"user_id": "f51f3683-7758-402e-9cf4-785f840d8738"},
        {"age": "60", "subject": "Приветственное письмо", "username": "vasya"},
        DeliveryChannel.EMAIL.value,
        DeliveryType.NOT_NIGHT.value,
        "ugc_service",
    )

    new_delivery = await test_database.pool.fetchrow(
        """SELECT *
            FROM deliveries
            WHERE delivery_id=$1;
        """,
        delivery_id,
    )
    assert new_delivery["delivery_id"] == delivery_id
    assert new_delivery["recipient"] == {
        "user_id": "f51f3683-7758-402e-9cf4-785f840d8738"
    }
    assert new_delivery["tz"] is None

    message = {"delivery_id": delivery_id, "event": EventType.CREATED}
    bytes_string = json.dumps(message).encode("utf-8")

    await notifications_enricher_service.main(bytes_string)

    enriched_delivery = await test_database.pool.fetchrow(
        """SELECT *
            FROM deliveries
            WHERE delivery_id=$1;
        """,
        delivery_id,
    )
    assert enriched_delivery["delivery_id"] == delivery_id
    assert enriched_delivery["recipient"] == {
        "user_id": "f51f3683-7758-402e-9cf4-785f840d8738",
        "email": "123@123.ru",
    }
    assert enriched_delivery["tz"] == "-8"


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [NOTIFICATIONS_TABLES], indirect=True)
async def test_notifications_enricher_consumer_send_event_ok(
    test_database,
    monkeypatch,
    notifications_enricher_service,
    mock_auth_api_ok,
):
    delivery_id = await test_database.pool.fetchval(
        """INSERT INTO deliveries(template_id, recipient, parameters, channel, "type", sender)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING delivery_id;
            """,
        123,
        {"user_id": "f51f3683-7758-402e-9cf4-785f840d8738"},
        {"age": "60", "subject": "Приветственное письмо", "username": "vasya"},
        DeliveryChannel.EMAIL.value,
        DeliveryType.IMMEDIATELY.value,
        "ugc_service",
    )

    message = {"delivery_id": delivery_id, "event": EventType.CREATED}
    bytes_string = json.dumps(message).encode("utf-8")

    async def mock(*args, **kwargs):
        sender = AMQPSenderPikaConnector(config={})
        sender.amqp_sender = AsyncMock()
        sender.setup = AsyncMock()
        await sender.amqp_sender.send(
            message=message,
            routing_key="event.send",
        )

    monkeypatch.setattr(
        "src.workers.consumers.notifications_enricher_consumer.service.NotificationsEnricherService.send_message",
        mock,
    )

    await notifications_enricher_service.main(bytes_string)

    delivery_distribution = await test_database.pool.fetchrow(
        """SELECT *
            FROM delivery_distributions
            WHERE delivery_id=$1;
        """,
        delivery_id,
    )
    assert delivery_distribution["delivery_id"] == delivery_id
    assert delivery_distribution["status"] == DeliveryStatus.CREATED
