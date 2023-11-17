from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithms: str
    secret_api_key: str


def get_settings() -> Settings:
    return Settings()


settings = Settings()
