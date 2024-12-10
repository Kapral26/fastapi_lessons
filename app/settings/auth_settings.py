"""
Настройки проекта.

Этот модуль определяет две модели данных: **AuthJWT** и **Settings**.

Модель **AuthJWT** отвечает за параметры конфигурации для работы с JWT-токенами:
- Пути к приватному и публичному ключам.
- Алгоритм шифрования.
- Время жизни токена.

Модель **Settings** используется для настройки всего приложения, включая параметры из модели **AuthJWT**.
"""

from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, field_validator, Field

from app.settings.exceptions import DoNotExistCertDirError, FileCertNotFoundError

# Определение базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

if not (BASE_DIR / "cert").exists():
    raise DoNotExistCertDirError


class AuthJWT(BaseModel):
    """
    Модель для настройки параметров работы с JWT-токенами.

    :param private_key_path: Путь к файлу с приватным ключом для подписания токенов.
    :param public_key_path: Путь к файлу с публичным ключом для проверки подписи токенов.
    :param algorithm: Алгоритм шифрования для JWT-токенов (по умолчанию "RS256").
    :param access_token_expire_minutes: Время жизни токена доступа в минутах (по умолчанию 3).
    """

    private_key_path: Annotated[Path, Field(validate_default=True)] = BASE_DIR / "cert" / "jwt-private.pem"
    public_key_path: Annotated[Path, Field(validate_default=True)] = BASE_DIR / "cert" / "jwt-public.pem"
    algorithm: str = "RS256"

    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    access_token_field: str = "type"
    access_token_type: str = "access"
    refresh_token_type: str = "refresh"

    @field_validator("private_key_path", "public_key_path")
    @classmethod
    def check_cert_exists(cls, v: Path) -> Path:
        """Проверка наличия файла с приватным и публичным ключами."""
        if not v.exists():
            raise FileCertNotFoundError
        return v
