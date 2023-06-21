import pytest
from src.workers.models.delivery import (
    DeliveryChannel,
    DeliveryStatus,
    DeliveryType,
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
        {"user_id": "f51f3683-7758-402e-9cf4-785f840d8738"},
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
        "user_id": "f51f3683-7758-402e-9cf4-785f840d8738"
    }
    assert delivery["tz"] == "+3"

    distribution_id = await test_database.pool.fetchval(
        """INSERT INTO delivery_distributions (delivery_id, recipient, status)
            VALUES ($1, $2, $3)
            RETURNING id;
        """,
        delivery_id,
        delivery["recipient"],
        DeliveryStatus.CREATED,
    )

    distribution = await test_database.pool.fetchrow(
        """SELECT *
            FROM delivery_distributions
            WHERE id = $1
        """,
        distribution_id,
    )
    assert distribution["recipient"] == {
        "user_id": "f51f3683-7758-402e-9cf4-785f840d8738"
    }
    assert distribution["status"] == DeliveryStatus.CREATED
