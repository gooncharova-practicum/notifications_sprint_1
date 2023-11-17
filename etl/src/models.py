from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, validator


class Notification(BaseModel):
    id_: UUID = Field(alias="id")
    is_instant: bool
    schedule_at: datetime
    layot: str
    subject: str
    body: str
    users_count: int
    users: list | None = None

    @validator("id_")
    def convert_uuid_to_str(cls, v: UUID) -> str:
        return str(v)


class UserDetail(BaseModel):
    id_: UUID = Field(alias="id")
    username: str
    email: str
    first_name: str
    last_name: str
    timezone: str
