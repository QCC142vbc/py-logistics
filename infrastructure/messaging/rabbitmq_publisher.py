import json
from typing import Callable, Awaitable

import pika


class RabbitMQPublisher:
    def __init__(self, host: str, queue: str) -> None:
        self._host = host
        self._queue = queue
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None

    def connect(self) -> None:
        """Connect to RabbitMQ."""
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue)

    def publish(self, message: dict) -> None:
        """Publish a message to the queue."""
        if not self._channel:
            raise RuntimeError("RabbitMQ not connected")
        
        self._channel.basic_publish(
            exchange="",
            routing_key=self._queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def close(self) -> None:
        """Close the connection."""
        if self._connection:
            self._connection.close()
