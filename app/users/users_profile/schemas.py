from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    Модель данных для пользователя.

    Атрибуты:
    username (str): Имя пользователя.
    password (str): Пароль пользователя.

    Класс Config:
    from_attributes (bool): Флаг, указывающий, что атрибуты модели должны быть получены из атрибутов класса.
    """

    username: str
    password: str

    class Config:
        """
        Класс Config используется для настройки поведения модели.

        Атрибуты:
        from_attributes (bool): Флаг, указывающий, что атрибуты модели должны быть получены из атрибутов класса.
        """

        from_attributes = True
