"""Модели связанные с токенами"""

from pydantic import BaseModel


class TokenResponseInfo(BaseModel):
    """
    Модель данных для информации о токене.

    :param access_token: Сгенерированный JWT-токен.
    :param refresh_token: Необязательный параметр. Токен для обновления доступа.
    :param token_type: Тип токена (например, "Bearer").
    """

    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
