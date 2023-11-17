from dependency_injector import containers, providers

from services.notifications import NotificationService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    notification_service = providers.Singleton(NotificationService)
