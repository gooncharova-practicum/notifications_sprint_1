#  type: ignore
import pika
from pydantic import BaseSettings


class Settings(BaseSettings):
    pg_host: str
    pg_port: int
    pg_db: str
    pg_user: str
    pg_password: str

    rmq_host: str
    rmq_port: int
    rmq_user: str
    rmq_password: str

    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    chunk_size: int = 100
    latest_check: str | None = None


settings = Settings()

pg_settings = {
    "host": settings.pg_host,
    "port": settings.pg_port,
    "dbname": settings.pg_db,
    "user": settings.pg_user,
    "password": settings.pg_password,
}

redis_settings = {
    "host": settings.redis_host,
    "port": settings.redis_port,
    "db": settings.redis_db,
    "password": settings.redis_password,
    "decode_responses": True,
}

rabbitmq_settings = {
    "host": settings.rmq_host,
    "port": settings.rmq_port,
    "virtual_host": "/",
    "credentials": pika.PlainCredentials(settings.rmq_user, settings.rmq_password),
}
