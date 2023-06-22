import datetime

from src.api.models.delivery import DeliveryResponse


test_recipient = {
    "email": "test@ya.ru",
    "user_id": "f51f3683-7758-402e-9cf4-785f840d8738",
}
test_parameters = {
    "age": "60",
    "subject": "Приветственное письмо",
    "username": "vasya",
}


def mock_create_delivery(
    delivery_id=1,
    template_id=123,
    recipient=None,
    parameters=None,
    channel="email",
    type="not_night",
    excluded=False,
    exclude_reason=None,
    sender="ugs_service",
    created_dt=None,
    updated_dt=None,
    tz=None,
):
    row_data = dict(
        delivery_id=delivery_id,
        template_id=template_id,
        channel=channel,
        type=type,
        excluded=excluded,
        exclude_reason=exclude_reason,
        sender=sender,
        created_dt=created_dt,
        updated_dt=updated_dt,
        tz=tz,
    )
    if not recipient:
        row_data["recipient"] = test_recipient
    if not parameters:
        row_data["parameters"] = test_parameters
    if not created_dt:
        row_data["created_dt"] = datetime.datetime(
            2023, 6, 22, 7, 47, 38, 309810, tzinfo=datetime.timezone.utc
        )
    if not updated_dt:
        row_data["updated_dt"] = datetime.datetime(
            2023, 6, 22, 7, 47, 38, 309810, tzinfo=datetime.timezone.utc
        )
    return DeliveryResponse.parse_obj(row_data) if row_data else None


def get_delivery_by_id():
    pass


def unsubscribe_user():
    pass


def get_deliveries_response(
    delivery_id=1,
    template_id=123,
    recipient=None,
    parameters=None,
    channel="email",
    type="not_night",
    sender="ugs_service",
    status=None,
    created_dt=None,
    updated_dt=None,
):
    if not recipient:
        recipient = test_recipient
    if not parameters:
        parameters = test_parameters
    if not created_dt:
        created_dt = "2023-06-22T07:47:38.309810+00:00"
    if not updated_dt:
        updated_dt = "2023-06-22T07:47:38.309810+00:00"
    return {
        "success": True,
        "result": {
            "delivery_id": delivery_id,
            "template_id": template_id,
            "recipient": recipient,
            "channel": channel,
            "parameters": parameters,
            "type": type,
            "sender": sender,
            "status": status,
            "created_dt": created_dt,
            "updated_dt": updated_dt,
        },
        "errors": None,
    }
