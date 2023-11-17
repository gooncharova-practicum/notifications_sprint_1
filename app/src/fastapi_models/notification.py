from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class NotificationOut(BaseModel):
    id_: UUID = Field(alias="id")
    message_id: UUID
    template_id: UUID
    is_instant: bool
    status: str
    schedule_at: datetime
    users_ids: list[UUID]
    created_at: datetime
    modified_at: datetime
    additional_info: dict | None

    class Config:
        orm_mode = True


class NotificationData(BaseModel):
    user_id: UUID
    event_name: str
    add_info: dict | None
