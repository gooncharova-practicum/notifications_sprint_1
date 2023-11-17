import json
from typing import Any as AnyType

from redis import Redis


class RedisClient:
    def __init__(
        self,
        redis_connection: Redis,
    ) -> None:
        self.redis = redis_connection

    def get(self, key: str) -> AnyType:
        if value := self.redis.get(key):
            return json.loads(value)
        return value

    def set(self, key: str, value: AnyType) -> None:
        value = json.dumps(value)
        self.redis.set(key, value)

    def increment(self, key: str, amount: int = 1) -> None:
        self.redis.incr(key, amount=amount)

    def delete(self, key: str) -> None:
        self.redis.delete(key)
