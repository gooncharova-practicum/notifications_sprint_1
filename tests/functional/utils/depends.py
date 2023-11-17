import uuid
from datetime import datetime, timezone

import aiopg

from config import settings
from utils.jwt import generate_acess_token

ACCESS_TOKEN = generate_acess_token()
ACCESS_TOKEN_INVALID = generate_acess_token(invalid=True)

HEADER_WITH_TOKEN = {"Access-Token": f"{ACCESS_TOKEN}"}
HEADER_WITH_INDVALID_TOKEN = {"Access-Token": f"{ACCESS_TOKEN_INVALID}"}

NOTIFICATION_UUID = str(uuid.uuid4())

TEMPLATE_UUID = str(uuid.uuid4())
TEMPLATE_NAME = "test_template"
TEMPLATE_DESCRIPTION = "test_template_description"
TEMPLATE_LAYOT = """<h1 style="text-align: left; padding-left: 240px;">Добро пожаловать</h1>"""

MESSAGE_UUID = str(uuid.uuid4())
MESSAGE_NAME = "test_message"
MESSAGE_SUBJECT = "test_subj"
MESSAGE_BODY = "test_body"

NOTIFICATION_UUID = str(uuid.uuid4())
USER_UUID = str(uuid.uuid4())
USER_UUID_ARRAY = f"{{{USER_UUID}}}"
ADD_INFO: dict[str, str] = {}

DATETIME_NOW = datetime.now(tz=timezone.utc)


async def create_template() -> None:
    pool = await aiopg.create_pool(settings.DB_DSN)
    async with pool.acquire() as conn, conn.cursor() as cur:
        await cur.execute(
            "INSERT INTO notify.templates "
            "(id, created_at, modified_at, name, description, layot) "
            f"VALUES ('{TEMPLATE_UUID}', '{DATETIME_NOW}', '{DATETIME_NOW}', "
            f"'{TEMPLATE_NAME}', '{TEMPLATE_DESCRIPTION}', '{TEMPLATE_LAYOT}');"
        )


async def create_message() -> None:
    pool = await aiopg.create_pool(settings.DB_DSN)
    async with pool.acquire() as conn, conn.cursor() as cur:
        await cur.execute(
            "INSERT INTO notify.messages (id, created_at, modified_at, name, subject, body) "
            f"VALUES ('{MESSAGE_UUID}', '{DATETIME_NOW}', '{DATETIME_NOW}', '{MESSAGE_NAME}', "
            f"'{MESSAGE_SUBJECT}', '{MESSAGE_BODY}');"
        )


async def create_notification() -> None:
    pool = await aiopg.create_pool(settings.DB_DSN)
    async with pool.acquire() as conn, conn.cursor() as cur:
        await cur.execute(
            """INSERT INTO notify.notifications """
            """(id, created_at, modified_at, template_id, message_id, status, """
            """users_ids, is_instant, schedule_at) """
            f"""VALUES ('{NOTIFICATION_UUID}', '{DATETIME_NOW}', '{DATETIME_NOW}', """
            f"""'{TEMPLATE_UUID}', '{MESSAGE_UUID}', 'CREATED', '{USER_UUID_ARRAY}', """
            f"""True, '{DATETIME_NOW}');"""
        )
