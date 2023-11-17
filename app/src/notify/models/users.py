from django.db import models
from django.utils.translation import gettext_lazy as _
from psqlextra.indexes import UniqueIndex

from .mixins import TimeStampedMixin, UUIDMixin


class User(UUIDMixin, TimeStampedMixin):
    username = models.CharField(_("username"), unique=True, max_length=80)
    email = models.EmailField(_("email"), unique=True, max_length=120)

    class Meta:
        db_table = 'notify"."users'
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return str(self.username)


class UserInfo(UUIDMixin, TimeStampedMixin):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="info",
    )
    first_name = models.CharField(_("first_name"), max_length=64)
    last_name = models.CharField(_("last_name"), max_length=64)
    timezone = models.CharField(_("timezone"))

    class Meta:
        db_table = 'notify"."users_info'
        verbose_name = _("User info")
        verbose_name_plural = _("Users info")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "first_name", "last_name"],
                name="unique_first_last_name_for_user_id",
            )
        ]
        indexes = [
            UniqueIndex(
                fields=["user", "first_name", "last_name"],
                name="info_user_first_last_name_idx",
            ),
        ]

    def __str__(self) -> str:
        return str(f"{self.user.username}: {self.first_name} {self.last_name}")
