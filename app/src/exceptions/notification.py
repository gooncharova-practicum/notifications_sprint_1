class NotificationAlreadyExistsError(Exception):
    def __init__(self) -> None:
        super().__init__("Notification already exists")


class NotFoundNameError(Exception):
    def __init__(self, entity: str, obj_name: str) -> None:
        super().__init__(f"{entity} with name: {obj_name} not found")
