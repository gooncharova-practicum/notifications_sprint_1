from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    rabbit_host: str
    rabbit_user: str
    rabbit_passwd: str
    exchange: str
    instant_queue: str
    scheduled_queue: str
    instant_key: str
    scheduled_key: str
    mailer_host: str
    mailer_port: str
    mailer_user: str
    mailer_passwd: str
    mailer_sender: str

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()


settings = Settings()
