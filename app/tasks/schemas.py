from pydantic import BaseModel, field_validator, model_validator


class TaskCreateSchema(BaseModel):
    """
    Этот класс представляет схему для создания задачи.

    Атрибуты:
    - name (str, optional): The name of the task. Defaults to None.
    - pomodoro_count (int): The number of pomodoros for the task.
    - category_id (int, optional): The ID of the category for the task. Defaults to None.
    """

    name: str | None = None
    pomodoro_count: int
    category_id: int | None = None


class TaskSchema(TaskCreateSchema):
    """
    Модель данных для задачи.

    id (int | None): Идентификатор задачи.
    name (str | None): Имя задачи.
    pomodoro_count (int): Количество помидоров.
    category_id (int | None): Идентификатор категории.

    Методы:
    name_or_category_is_not_empty(cls, value: str | int | None) -> None | str | int:
         Проверяет, что имя или идентификатор категории не пустые.
    model_trigger_after(self) -> None: Запускает триггер после инициализации модели.
    """

    id: int | None = None
    user_id: int

    # noinspection PyNestedDecorators
    @field_validator("pomodoro_count", "category_id")
    @classmethod
    def name_or_category_is_not_empty(cls, value: str | int | None) -> None | str | int:  # noqa: ANN102
        """
        Проверяет, что имя или идентификатор категории не пустые.

        Аргументы:
        - value: Значение для проверки.

        Возвращает:
        - Значение, если оно не пустое.
        """
        return 111 if not value else value

    @model_validator(mode="after")  # mode = 'before' - до инициализации модели.
    def model_trigger_after(self):  # noqa: ANN201
        """
        Запускает триггер после инициализации модели.

        Возвращает:
        - Модель после обработки.
        """
        self.name = "Пустая задача" if not self.name else self.name
        return self

    class Config:
        """Класс необходимый для преобразования ORM-объекта в модель."""

        from_attributes = True


class CategorySchema(BaseModel):
    """
    Модель категории.

    Атрибуты:
    category_id (int): Идентификатор категории.
    name (str): Имя категории.
    """

    category_id: int
    name: str
