import json
import logging

import backoff
import pika
from pika.exceptions import (
    AMQPConnectionError,
    ConnectionClosed,
    StreamLostError,
)


logger = logging.getLogger(__name__)


class RabbitMQ:
    def __init__(
        self, host: str, port: int, username: str, password: str, queue: str
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue = queue
        self.channel = None

    @backoff.on_exception(backoff.expo, AMQPConnectionError)
    def connect(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=pika.PlainCredentials(
                    self.username,
                    self.password,
                ),
            )
        )
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    @backoff.on_exception(backoff.expo, [ConnectionClosed, StreamLostError])
    def publish(self, message):
        if self.channel is None or self.channel.is_closed:
            logger.info("Reconnected RabbitMQ")
            self.connect()

        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        logger.info("Channel %s: Sent %s" % (self.channel, message))

    def start_consuming(self, callback):
        if self.channel is None or self.channel.is_closed:
            logger.info("Reconnected RabbitMQ")
            self.connect()

        self.channel.basic_consume(
            queue=self.queue, on_message_callback=callback
        )
        logger.info("Channel %s is waiting for messages" % self.channel)
        self.channel.start_consuming()
