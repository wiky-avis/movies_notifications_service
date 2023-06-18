from typing import Optional

from notifications_api.src.common.clients.amqp_sender import AMQPSenderPika
from notifications_api.src.settings import notifications_amqp_settings


class AMQPSenderPikaConnector:
    amqp_sender: Optional[AMQPSenderPika] = None

    @classmethod
    async def setup(cls):
        cls.amqp_sender = AMQPSenderPika(
            settings=notifications_amqp_settings.dict()
        )
        await cls.amqp_sender.setup()

    @classmethod
    async def close(cls):
        if cls.amqp_sender:
            await cls.amqp_sender.close()
            cls.amqp_sender = None
