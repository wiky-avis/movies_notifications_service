import asyncio
from unittest.mock import AsyncMock

import pytest
from src.common.connectors.amqp import AMQPSenderPikaConnector
from src.workers.models.delivery import (
    DeliveryChannel,
    DeliveryType,
    EventType,
)
from tests.vars.constants import DELIVERIES
from tests.vars.tables import NOTIFICATIONS_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [NOTIFICATIONS_TABLES], indirect=True)
async def test_delivery_trigger_starter_ok(
    test_database,
    monkeypatch,
    delivery_trigger_starter_service,
):
    tasks = [
        test_database.pool.execute(
            """INSERT INTO deliveries(template_id, recipient, parameters, channel, "type", sender, tz)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING delivery_id;
        """,
            delivery["template_id"],
            delivery["recipient"],
            delivery["parameters"],
            DeliveryChannel.EMAIL.value,
            DeliveryType.NOT_NIGHT.value,
            "ugc_service",
            delivery["tz"],
        )
        for delivery in DELIVERIES
    ]

    await asyncio.gather(*tasks)

    for delivery_id in tasks:
        message = {"delivery_id": delivery_id, "event": EventType.SEND}

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

    data = await test_database.pool.fetch(
        """SELECT *
            FROM delivery_distributions
            ORDER BY recipient;
        """
    )
    distributions = [item["recipient"] for item in data]
    assert distributions == [
        {
            "email": "test4@ya.ru",
            "user_id": "e47f4f3e-9ae0-45c8-81fa-b3de71c7e478",
        },
        {
            "email": "test7@ya.ru",
            "user_id": "6735bf49-7add-4411-807c-36f5549a189d",
        },
        {
            "email": "test8@ya.ru",
            "user_id": "3faf86b5-202d-4ef6-a46c-3831a77f7b6a",
        },
        {
            "email": "test9@ya.ru",
            "user_id": "f51f3683-7758-402e-9cf4-785f840d8738",
        },
    ]
