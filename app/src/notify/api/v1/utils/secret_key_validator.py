from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError

from core.containers import Container

access_token_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Access is denied",
)


class SecretApiKey(BaseModel):
    secret_api_key: str
    datetime_now: str


@inject
async def valid_secret_key(
    access_token: str = Header(),  # Noqa
    jwt_secret_key: str = Depends(Provide[Container.config.jwt_secret_key]),
    jwt_algorithms: str = Depends(Provide[Container.config.jwt_algorithms]),
    secret_api_key: str = Depends(Provide[Container.config.secret_api_key]),
) -> None:
    """Проверка секретного ключа"""

    try:
        key = jwt.decode(
            access_token,
            jwt_secret_key,
            algorithms=jwt_algorithms.split(","),
        )
        key = SecretApiKey(**key)  # type: ignore
    except (JWTError, ValidationError):
        raise access_token_exception

    if key.secret_api_key != secret_api_key:
        raise access_token_exception
