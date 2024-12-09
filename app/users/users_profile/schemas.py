from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True

    class Config:
        """
        Класс Config используется для настройки поведения модели.

        Атрибуты:
        from_attributes (bool): Флаг, указывающий, что атрибуты модели должны быть получены из атрибутов класса.
        """

        from_attributes = True
