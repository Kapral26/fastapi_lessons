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
    detail = "Token expired"


class TokenIsNotCorrectError(Exception):
    detail = "Token is not correct"

class TaskNotFoundError(Exception):
    detail = "Task not found"