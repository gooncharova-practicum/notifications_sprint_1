import logging
import time
from contextlib import closing

import backoff
import pika
import pika.exceptions
import psycopg
import redis

from clients.pg import PostgresExtractor
from clients.redis import Redis, RedisClient
from clients.rmq import RabbitPublisher
from config import pg_settings, rabbitmq_settings, redis_settings, settings  # type: ignore
from etl import ETL  # type: ignore

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


@backoff.on_exception(
    backoff.expo,
    (
        pika.exceptions.AMQPConnectionError,
        psycopg.errors.ConnectionException,
        redis.exceptions.ConnectionError,
    ),
)
def main() -> None:
    with psycopg.connect(**pg_settings) as pg_conn, closing(
        pika.BlockingConnection(pika.ConnectionParameters(**rabbitmq_settings))
    ) as rmq_conn:
        pg_extractor = PostgresExtractor(
            settings.chunk_size,  # type: ignore[attr-defined]
            pg_conn,
        )
        redis_client = RedisClient(Redis(**redis_settings))
        rabbitmq_publisher = RabbitPublisher(rmq_conn)

        etl = ETL(
            pg_extractor=pg_extractor,
            redis_client=redis_client,
            rabbitmq_publisher=rabbitmq_publisher,
            chunk_size=settings.chunk_size,  # type: ignore [attr-defined]
            latest_check=settings.latest_check,  # type: ignore [attr-defined]
        )
        while True:
            try:
                etl.check_n_transfer()
            except (
                pika.exceptions.ChannelClosed,
                psycopg.errors.DataError,
                redis.exceptions.DataError,
            ):
                time.sleep(1)


main()
