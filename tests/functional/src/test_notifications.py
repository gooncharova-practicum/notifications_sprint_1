import uuid
from http import HTTPStatus

import pytest

from utils.depends import (
    HEADER_WITH_INDVALID_TOKEN,
    HEADER_WITH_TOKEN,
    NOTIFICATION_UUID,
    USER_UUID,
)

NOFICATONS_URL_PATH = "/notifications"
NOTIFICATION_BODY = {"user_id": f"{USER_UUID}", "event_name": "test"}

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ("method", "path", "headers", "expected_status"),
    [
        ("GET", NOFICATONS_URL_PATH + f"/{NOTIFICATION_UUID}", HEADER_WITH_TOKEN, HTTPStatus.OK),
        (
            "GET",
            NOFICATONS_URL_PATH,
            HEADER_WITH_TOKEN,
            HTTPStatus.METHOD_NOT_ALLOWED,
        ),
        (
            "GET",
            NOFICATONS_URL_PATH + f"/{str(uuid.uuid4())}",
            HEADER_WITH_TOKEN,
            HTTPStatus.NOT_FOUND,
        ),
        (
            "GET",
            NOFICATONS_URL_PATH + f"/{NOTIFICATION_UUID}",
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.FORBIDDEN,
        ),
    ],
)
async def test_get_notification(make_request, method, path, headers, expected_status) -> None:
    response = await make_request(method, path, headers=headers)
    assert response.status == expected_status


@pytest.mark.parametrize(
    ("method", "path", "body", "headers", "expected_status"),
    [
        (
            "POST",
            NOFICATONS_URL_PATH,
            NOTIFICATION_BODY,
            HEADER_WITH_TOKEN,
            HTTPStatus.CREATED,
        ),
        (
            "POST",
            NOFICATONS_URL_PATH,
            None,
            HEADER_WITH_TOKEN,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            "POST",
            NOFICATONS_URL_PATH,
            None,
            HEADER_WITH_INDVALID_TOKEN,
            HTTPStatus.FORBIDDEN,
        ),
    ],
)
async def test_create_notification(
    make_request, method, path, body, headers, expected_status
) -> None:
    response = await make_request(method, path, headers=headers, body=body)
    assert response.status == expected_status
