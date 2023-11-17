from collections.abc import Iterator, Sequence
from datetime import datetime
from typing import Any as AnyType
from typing import TypeVar
from uuid import UUID

import psycopg
from psycopg.abc import Query
from psycopg.rows import class_row

from models import Notification, UserDetail
from queries import NOTIFICATIONS_LATEST, USERS_DETAILED

M = TypeVar("M", Notification, UserDetail)


class PostgresExtractor:
    def __init__(
        self,
        chunk_size: int,
        postgres_connection: psycopg.Connection,
    ) -> None:
        self.postgres = postgres_connection
        self.chunk_size = chunk_size

    def _execute_iter(
        self,
        query: Query,
        params: Sequence | Sequence[Sequence] | None = None,
        model: AnyType | None = None,
    ) -> Iterator[list[M | AnyType]]:
        """Используется для потенциально больших запросов.

        Args:
          query: SQL запрос.
          params: Плейсхолдеры для SQL запроса.
            Можеть быть как простой список/кортеж, так и вложенный.
          model: pydantic.BaseModel либо dataclass.
        """
        if model:
            model = class_row(model)

        with self.postgres.cursor(row_factory=model) as cur:
            data = cur.execute(query, params)
            while data_chunked := data.fetchmany(self.chunk_size):
                yield data_chunked

    def get_new_notifications(self, date_: datetime, offset: int) -> Iterator[list[M]]:
        return self._execute_iter(
            query=NOTIFICATIONS_LATEST, params=(date_, offset), model=Notification
        )

    def get_users_by_notification_id(
        self, notification_id: str | UUID, offset: int
    ) -> Iterator[list[M]]:
        return self._execute_iter(
            query=USERS_DETAILED, params=(notification_id, offset), model=UserDetail
        )
