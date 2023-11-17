from datetime import datetime, timezone

from jose import jwt

from config import settings


def generate_acess_token(*, invalid: bool = False) -> str:
    token_data = {
        "secret_api_key": settings.secret_api_key if not invalid else "111222333qqq",
        "datetime_now": str(datetime.now(tz=timezone.utc)),
    }
    return jwt.encode(token_data, settings.jwt_secret_key, settings.jwt_algorithms)
