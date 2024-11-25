class UserNotFoundError(Exception):
    """Пользователь не найден."""

    detail = "User not found"


class UserInvalidError(Exception):
    """Пользователь не найден."""

    detail = "User password invalid"
