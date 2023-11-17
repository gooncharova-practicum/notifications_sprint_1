from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException, status

from core.containers import Container
from exceptions.notification import NotFoundNameError, NotificationAlreadyExistsError
from fastapi_models.notification import NotificationData, NotificationOut
from notify.api.v1.utils.secret_key_validator import SecretApiKey, valid_secret_key
from services.notifications import NotificationService

router = APIRouter()


@router.get(
    "/{notification_id}",
    response_model=NotificationOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(valid_secret_key)],
    summary="Получить уведомление по id",
)
@inject
async def get_notification(
    notification_id: UUID,
    notification_service: NotificationService = Depends(Provide[Container.notification_service]),
) -> NotificationOut:
    notification = await notification_service.get(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        ) from None
    return notification  # type: ignore


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=NotificationOut,
    dependencies=[Depends(valid_secret_key)],
    summary="Создать уведомление",
)
@inject
async def create_notification(
    notification_data: NotificationData,
    notification_service: NotificationService = Depends(Provide[Container.notification_service]),
) -> NotificationOut:
    user_id = notification_data.user_id
    event_name = notification_data.event_name
    add_info = notification_data.add_info if notification_data.add_info else {}

    try:
        notification = await notification_service.create(user_id, event_name, add_info)
    except NotFoundNameError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from None
    except NotificationAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from None
    return notification  # type: ignore
