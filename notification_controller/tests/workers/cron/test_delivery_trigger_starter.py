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
async def test_delivery_trigger_starter_ok(
    test_database,
    monkeypatch,
    delivery_trigger_starter_service,
):
    delivery_id = await test_database.pool.fetchval(
        """INSERT INTO deliveries(template_id, recipient, parameters, channel, "type", sender, tz)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING delivery_id;
        """,
        123,
        {
            "user_id": "f51f3683-7758-402e-9cf4-785f840d8738",
            "email": "123@123.ru",
        },
        {"age": "60", "subject": "Приветственное письмо", "username": "vasya"},
        DeliveryChannel.EMAIL.value,
        DeliveryType.NOT_NIGHT.value,
        "ugc_service",
        "+3",
    )
    delivery = await test_database.pool.fetchrow(
        """SELECT *
            FROM deliveries
            WHERE excluded = FALSE AND type = 'not_night' AND CAST(tz AS INTEGER) BETWEEN -7 AND 6
        """
    )
    assert delivery["delivery_id"] == delivery_id
    assert delivery["recipient"] == {
        "user_id": "f51f3683-7758-402e-9cf4-785f840d8738",
        "email": "123@123.ru",
    }
    assert delivery["tz"] == "+3"

    message = {"delivery_id": delivery_id, "event": EventType.CREATED}

    async def mock(*args, **kwargs):
        sender = AMQPSenderPikaConnector(config={})
        sender.amqp_sender = AsyncMock()
        sender.setup = AsyncMock()
        await sender.amqp_sender.send(
            message=message,
            routing_key="event.send",
        )

    monkeypatch.setattr(
        "src.workers.cron.delivery_trigger_starter.service.DeliveryTriggerStarterService.send_message",
        mock,
    )

    await delivery_trigger_starter_service.main()

    distribution = await test_database.pool.fetchrow(
        """SELECT *
            FROM delivery_distributions
            WHERE delivery_id = $1
        """,
        delivery_id,
    )
    assert distribution["recipient"] == {
        "user_id": "f51f3683-7758-402e-9cf4-785f840d8738",
        "email": "123@123.ru",
    }
    assert distribution["status"] == DeliveryStatus.CREATED
