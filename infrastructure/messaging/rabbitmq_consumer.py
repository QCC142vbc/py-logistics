import json
from typing import Callable, Awaitable

import pika


class RabbitMQConsumer:
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

    async def consume(self, handler: Callable[[dict], Awaitable[None]]) -> None:
        """Consume messages from the queue."""
        if not self._channel:
            raise RuntimeError("RabbitMQ not connected")

        def callback(ch, method, properties, body):
            message = json.loads(body)
            # In a real async implementation, this would use aio-pika
            # For now, we'll call the handler synchronously
            import asyncio
            asyncio.create_task(handler(message))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=callback,
        )
        self._channel.start_consuming()

    def close(self) -> None:
        """Close the connection."""
        if self._connection:
            self._connection.close()
