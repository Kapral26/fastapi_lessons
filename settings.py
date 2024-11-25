from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = Path(__file__).parent.absolute() / ".dev.env"


class Settings(BaseSettings):
    """Класс настроек."""

    # Желательно вместо str использовать SecretStr
    # для конфиденциальных данных, например, токена бота

    sqlite_db_name: str = Field(..., alias="SQLITE_DB_NAME")

    postgres_user: str = Field(
        ..., alias="POSTGRES_USER"
    )  # Имя пользователя базы данных
    postgres_password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")
    # Пароль пользователя, хранится как SecretStr для безопасности
    postgres_db: str = Field(..., alias="POSTGRES_DB")  # Название базы данных
    postgres_host: str = Field(..., alias="POSTGRES_HOST")  # Хост-сервера базы данных
    postgres_port: int = Field(..., alias="POSTGRES_PORT")  # Порт сервера базы данных
    debug: bool = Field(..., alias="DEBUG")

    redis_host: str = Field(..., alias="REDIS_HOST")
    redis_port: int = Field(..., alias="REDIS_PORT")
    redis_db: int = Field(..., alias="REDIS_DB")

    # Свойства, которые генерируют URL-адреса подключения к PostgreSQL с использованием разных драйверов
    @property
    def database_dsn(self) -> str:
        """Возвращает объект URL для подключения к PostgreSQL с использованием sqlalchemy и драйвера psycopg2."""
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def async_database_dsn(self) -> str:
        """Возвращает объект URL для подключения к PostgreSQL с использованием sqlalchemy и драйвера psycopg2."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # Начиная со второй версии pydantic, настройки класса настроек задаются
    # через model_config
    # В данном случае будет использоваться файла .env, который будет прочитан
    # с кодировкой UTF-8
    model_config = SettingsConfigDict(env_file=dotenv_path, env_file_encoding="utf-8")


# При импорте файла сразу создастся
# и провалидируется объект конфига,
# который можно далее импортировать из разных мест

if __name__ == "__main__":
    config = Settings()
    a = 1
