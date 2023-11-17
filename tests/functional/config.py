from pydantic import BaseSettings


class Settings(BaseSettings):
    notification_host: str = "test-app-api"
    notification_port: int = 8000
    notification_api_prefix: str = "api/v1"
    notification_url: str | None = None

    jwt_secret_key: str
    jwt_algorithms: str
    secret_api_key: str

    DB_DSN: str

    def __init__(self, **data: dict) -> None:  # type: ignore [arg-type]
        super().__init__(**data)  # type: ignore [arg-type]
        self.notification_url = f"http://{self.notification_host}:{self.notification_port}/{self.notification_api_prefix}"


settings = Settings()
