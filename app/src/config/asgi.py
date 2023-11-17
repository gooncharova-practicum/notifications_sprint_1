import os

from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from config import settings
from core.config import Settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def get_fastapi_application() -> FastAPI:
    from core.containers import Container
    from notify.api.v1 import notifications

    container = Container()
    container.config.from_pydantic(Settings())
    container.wire(packages=["notify.api.v1"])

    app = FastAPI(
        title=settings.FASTAPI_PROJECT_TITLE,  # type: ignore [arg-type]
        description=settings.FASTAPI_PROJECT_DESCRIPTION,  # type: ignore [arg-type]
        version=settings.FASTAPI_PROJECT_VERSION,  # type: ignore [arg-type]
        docs_url=settings.FASTAPI_DOCS_URL,
        openapi_url=settings.FASTAPI_OPENAPI_URL,
        default_response_class=ORJSONResponse,
    )

    app.container = container
    app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Уведомления"])

    return app


django_application = get_asgi_application()
fastapi_application = get_fastapi_application()
