from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from psqlextra.indexes import UniqueIndex
from tinymce.models import HTMLField

from .mixins import TimeStampedMixin, UUIDMixin


class Template(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    layot = HTMLField(_("layot"))

    class Meta:
        db_table = 'notify"."templates'
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")
        indexes = [
            UniqueIndex(
                fields=["name", "layot"],
                name="template_name_layot_idx",
            ),
        ]

    def __str__(self) -> str:
        return str(self.name)


class Message(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    subject = models.CharField(_("subject"), max_length=255)
    body = models.TextField(_("body"), blank=True)

    class Meta:
        db_table = 'notify"."messages'
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        indexes = [
            UniqueIndex(
                fields=["name", "subject", "body"],
                name="message_name_subject_body_idx",
            ),
        ]

    def __str__(self) -> str:
        return str(self.name)


class Notification(UUIDMixin, TimeStampedMixin):
    template = models.ForeignKey(
        "Template",
        on_delete=models.CASCADE,
        verbose_name=_("Template"),
        related_name="notification",
    )
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, verbose_name=_("Message"), related_name="notification"
    )
    status = models.CharField(
        _("status"),
        default="CREATED",
        max_length=10,
        editable=False,
    )
    users_ids = ArrayField(models.UUIDField(), verbose_name=_("users_ids"))
    is_instant = models.BooleanField(_("is_instant"), default=True)  # type: ignore
    schedule_at = models.DateTimeField(
        _("schedule_at"),
        default=now,
        help_text=_(
            "Укажите в случае, если вы сняли галку в пункте 'Мгновенная отправка' "
            "и хотите отправить уведомление отложенно"
        ),
    )
    additional_info = models.JSONField(
        _("additional_info"),
        default={},
        null=True,
        blank=True,
        help_text=_(
            "Любая дополнительная информация для шаблона в формате ключ-значение, например "
            "{'user_from_id': 'c9212aef-0959-4b94-aee2-5cf9c9ae6bd1'}"
        ),
    )

    class Meta:
        db_table = 'notify"."notifications'
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        constraints = [
            models.UniqueConstraint(
                fields=["template", "message", "users_ids", "schedule_at"],
                name="unique_notification_for_users_ids",
            )
        ]
        indexes = [
            models.Index(fields=["created_at"], name="notification_created_idx"),
            models.Index(fields=["modified_at"], name="notification_modified_idx"),
        ]

    def __str__(self) -> str:
        return str(self.id)
