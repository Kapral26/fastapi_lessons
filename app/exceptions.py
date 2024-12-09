class UserNotFoundError(Exception):
    """
    Исключение, которое возникает, когда пользователь не найден.

    Атрибуты:
    detail (str): Сообщение об ошибке.
    """

    detail = "User not found"


class UserInvalidError(Exception):
    """
    Исключение, которое возникает, когда пароль пользователя неверный.

    Атрибуты:
    detail (str): Сообщение об ошибке.
    """

    detail = "User password invalid"


class TokenExpiredError(Exception):
    """Исключение, возникающее при истечении срока действия токена."""

    detail = "Token expired"


class TokenIsNotCorrectError(Exception):
    """Исключение, возникающее при некорректности токена."""

    detail = "Token is not correct"


class TaskNotFoundError(Exception):
    """Исключение, возникающее при отсутствии задачи."""

    detail = "Task not found"
