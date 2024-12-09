from fastapi import HTTPException
from starlette import status


class UnauthorisedError(HTTPException):
    """
    Исключение, возникающее при неудачной попытке авторизации.

    :param detail: Сообщение об ошибке, передаваемое клиенту.
                   По умолчанию "Incorrect username or password".
    """

    def __init__(self, detail: str = "Incorrect username or password"):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = detail
        self.headers = {"Authorization": f"Basic"}
        super().__init__(
                status_code=self.status_code,
                detail=self.detail,
                headers=self.headers
        )


class UserIsNotExistsError(HTTPException):
    """
    Исключение, возникающее при попытке обращения к несуществующему пользователю.

    :param detail: Сообщение об ошибке, передаваемое клиенту.
                   По умолчанию "User not found".
    """

    def __init__(self, detail: str = "User not found"):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail
        super().__init__(
                status_code=self.status_code,
                detail=self.detail
        )


class UserIsNotActiveError(HTTPException):
    """
    Исключение, возникающее при попытке взаимодействия с неактивным пользователем.

    :param detail: Сообщение об ошибке, передаваемое клиенту.
                   По умолчанию "User is not active".
    """

    def __init__(self, detail: str = "User is not active"):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = detail
        super().__init__(
                status_code=self.status_code,
                detail=self.detail,
        )


class InvalidAuthTokenError(HTTPException):
    """
    Исключение, возникающее при использовании недействительного токена авторизации.

    :param error_msg: Дополнительное сообщение об ошибке.
                      Если не указано, используется пустая строка.
    """

    def __init__(self, error_msg: str | None = None):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        error_msg = "" if not error_msg else f": {error_msg}"
        self.detail = "Invalid credentials" + error_msg
        super().__init__(status_code=self.status_code, detail=self.detail)
