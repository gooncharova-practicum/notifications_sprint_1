from uuid import UUID

from django.db import IntegrityError, models

from exceptions.notification import NotFoundNameError, NotificationAlreadyExistsError
from notify.models import Message, Notification, Template


class NotificationService:
    async def _get_object_by_name(
        self, model: models.Model, event_name: str
    ) -> Message | Template | None:
        return await model.objects.filter(name__icontains=event_name.lower()).afirst()

    async def create(self, user_id: UUID, event_name: str, add_info: dict) -> Notification:
        message = await self._get_object_by_name(Message, event_name)  # type: ignore [arg-type]
        if not message:
            msg = "Message"
            raise NotFoundNameError(msg, event_name)

        template = await self._get_object_by_name(Template, event_name)  # type: ignore [arg-type]
        if not template:
            msg = "Template"
            raise NotFoundNameError(msg, event_name) from None

        try:
            notification = await Notification.objects.acreate(
                template=template, message=message, users_ids=[user_id], additional_info=add_info
            )
        except IntegrityError:
            raise NotificationAlreadyExistsError from None

        return notification

    async def get(self, notification_id: UUID) -> Notification | None:
        return await Notification.objects.filter(pk=notification_id).afirst()
