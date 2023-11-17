from django.contrib import admin

from .models import Message, Notification, Template, User, UserInfo


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "modified_at")
    search_fields = ("id", "name", "description")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "subject", "created_at", "modified_at")
    search_fields = ("id", "name", "body", "subject")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "is_instant",
        "schedule_at",
        "template",
        "message",
        "created_at",
        "modified_at",
    )
    search_fields = ("id", "template", "message")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("id", "username", "email")


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "timezone")
    search_fields = ("id", "first_name", "last_name")
