import abc
import json
import smtplib
import typing

import backoff
import pika

from config import settings


class BaseTransport:
    @abc.abstractmethod
    def send(self, address_to: typing.Any, subject: str, message_body: str):  # Noqa
        pass


class EmailTransport(BaseTransport):
    @backoff.on_exception(backoff.expo, Exception)
    def send(self, address_to: typing.Any, subject: str, message_body: str) -> None:
        server = smtplib.SMTP(settings.mailer_host, settings.mailer_port)
        body = "\r\n".join(
            (
                f"From: {settings.mailer_sender}",
                f"To: {address_to}",
                f"Subject: {subject}",
                "",
                message_body,
            )
        )
        server.sendmail(settings.mailer_sender, address_to, body)
        server.close()


class Sender:
    def __init__(
        self,
        transport: BaseTransport,
    ) -> None:
        self.transport = transport

    def callback(
        self, ch: typing.Any, method: typing.Any, _: typing.Any, body: str, routing_key: str  # Noqa
    ) -> None:
        d_body = json.loads(body.decode("utf-8"))
        mail = d_body[routing_key]["data"]["params"]["condition"]["ticker"]["mail"]
        subj = d_body[routing_key]["data"]["params"]["condition"]["ticker"]["subject"]
        msg_body = d_body[routing_key]["data"]["params"]["condition"]["ticker"]["body"]
        self.transport(mail, subj, msg_body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @backoff.on_exception(backoff.expo, Exception)
    def queue_bind(self, queue_name: str, exchange: str, routing_key: str) -> None:
        credentials = pika.PlainCredentials(settings.rabbit_user, settings.rabbit_passwd)
        parameters = pika.ConnectionParameters(settings.rabbit_host, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_bind(queue=queue_name, exchange=exchange, routing_key=routing_key)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

        channel.start_consuming()


def get_sender() -> Sender:
    return Sender()


sender = Sender()
