import json

import backoff
import pika
import pika.exceptions
import pika.spec


class RabbitPublisher:
    def __init__(
        self,
        rabbitmq_connection: pika.BlockingConnection,
    ) -> None:
        self.rabbitmq = rabbitmq_connection

        self.channel = self.rabbitmq.channel()
        self.channel.queue_declare(queue="email_instant", durable=True)
        self.channel.queue_declare(queue="email_scheduled", durable=True)
        self.channel.exchange_declare(
            exchange="email_notify",
            exchange_type="x-delayed-message",
            durable=True,
            arguments={"x-delayed-type": "direct"},
        )
        self.channel.queue_bind(
            queue="email_instant", exchange="email_notify", routing_key="instant"
        )
        self.channel.queue_bind(
            queue="email_scheduled", exchange="email_notify", routing_key="scheduled"
        )

    @backoff.on_exception(backoff.expo, pika.exceptions.ChannelClosed)
    def publish(
        self, message: dict, *, headers: dict | None = None, instant: bool = True, delay: int = 0
    ) -> None:
        if not instant:
            headers = {"x-delay": delay}
            routing_key = "scheduled"
        else:
            routing_key = "instant"

        self.channel.basic_publish(
            exchange="email_notify",
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                headers=headers,
            ),
        )
