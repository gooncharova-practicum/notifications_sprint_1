import logging
from datetime import datetime

import pytz

from clients.pg import PostgresExtractor
from clients.redis import RedisClient
from clients.rmq import RabbitPublisher
from models import Notification
from utils import get_delay_in_ms

logger = logging.getLogger(__name__)

REDIS_KEY_LAST_CHECK = "E1_BACKLOG_LAST_CHECK"
REDIS_KEY_N_OFFSET = "E1_BACKLOG_NOTIFICATIONS_OFFSET"
REDIS_KEY_U_OFFSET = "E1_BACKLOG_NOTIFICATIONS_OFFSET_USERS"


class ETL:
    def __init__(
        self,
        redis_client: RedisClient,
        pg_extractor: PostgresExtractor,
        rabbitmq_publisher: RabbitPublisher,
        chunk_size: int,
        latest_check: str | None,
    ) -> None:
        self.redis_client = redis_client
        self.pg_extractor = pg_extractor
        self.rmq_publisher = rabbitmq_publisher
        self.chunk_size = chunk_size
        if not latest_check:
            self.latest_check = datetime.now(tz=pytz.utc).replace(tzinfo=None).isoformat()
        else:
            self.latest_check = latest_check

        logger.info("ETL started")

    def check_n_transfer(self) -> None:
        latest_check_date = self.redis_client.get(REDIS_KEY_LAST_CHECK) or self.latest_check
        notifications_offset = self.redis_client.get(REDIS_KEY_N_OFFSET) or 0

        for _pg_offset_notifications, notifications_batch in enumerate(
            self.pg_extractor.get_new_notifications(latest_check_date, notifications_offset),
            notifications_offset,
        ):
            logger.info("Find new notifications, count: %s", len(notifications_batch))
            self.process_notifications(notifications_batch)

        self.redis_client.set(REDIS_KEY_N_OFFSET, 0)
        self.redis_client.set(REDIS_KEY_LAST_CHECK, datetime.now(tz=pytz.utc).isoformat())

    def process_notifications(self, notifications: tuple[Notification]) -> None:
        for notification in notifications:
            logger.info("Processing notitification with id: %s", notification.id_)
            self.process_users_in_notification(notification)
            self.redis_client.increment(REDIS_KEY_N_OFFSET)

    def process_users_in_notification(self, notification: Notification) -> None:
        notifications_offset_users = self.redis_client.get(REDIS_KEY_U_OFFSET) or 0

        for offset_u, users in enumerate(
            self.pg_extractor.get_users_by_notification_id(
                notification.id_, notifications_offset_users
            ),
            notifications_offset_users,
        ):
            logger.info("Processing users from notification with id: %s", notification.id_)
            storage_users_by_delay = {}  # type: ignore

            for user in users:
                storage_users_by_delay.setdefault(
                    get_delay_in_ms(user.timezone, notification.schedule_at),
                    [],
                ).append(user.dict(exclude={"id_", "timezone"}))

            logger.info("Send message to queue, notification with id: %s", notification.id_)
            self.send_to_queue(notification, storage_users_by_delay)
            self.redis_client.set(REDIS_KEY_U_OFFSET, (offset_u + 1) * self.chunk_size)
        self.redis_client.set(REDIS_KEY_U_OFFSET, 0)

    def send_to_queue(self, notification: Notification, hashmap: dict) -> None:
        if notification.is_instant:
            notification.users = list(hashmap.values())
            self.rmq_publisher.publish(
                message=notification.dict(
                    by_alias=True, exclude={"is_instant", "schedule_at", "users_count"}
                ),
                instant=True,
            )
        else:
            for delay, users in hashmap.items():
                notification.users = users
                self.rmq_publisher.publish(
                    message=notification.dict(
                        by_alias=True, exclude={"is_instant", "schedule_at", "users_count"}
                    ),
                    instant=False,
                    delay=delay,
                )
