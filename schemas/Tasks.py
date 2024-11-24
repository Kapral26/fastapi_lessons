from pydantic import BaseModel, field_validator, model_validator


class TaskDTO(BaseModel):
    id: int | None = None
    name: str | None = None
    pomodoro_count: int
    category_id: int | None = None

    @field_validator("pomodoro_count", "category_id")
    @classmethod
    def name_or_category_is_not_empty(cls, value: str | int | None) -> None | str | int:
        """
        Проверка на пустоту названия или категории

        Он реализован не до конца корректно - для примера.
        Если поле не пустое, то возвращает его,
        иначе возвращает число 44

        Эта проверка происходит до инициализации модели
        """
        return 111 if not value else value

    @model_validator(mode="after")  # mode = 'before' - до инициализации модели.
    def model_trigger_after(self):
        """
        model_validator - Позволяет проверять модель целиком
        mode - указывает, когда это необходимо делать

        Раз мы проверяем модель целиком, то и возвращать мы должны модель.
        """
        self.name = "Пустая задача" if not self.name else self.name
        return self

    class Config:
        """Класс необходимый для преобразования ORM-объекта в модель."""

        from_attributes = True

class Category(BaseModel):
    category_id: int
    name: str
