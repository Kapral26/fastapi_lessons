"""Модуль фикстур для тестирования JWT."""

import pytest

from app.settings.main_settings import Settings
from app.users.auth.token.service import TokenService


@pytest.fixture
def mock_token_service() -> TokenService:
    """Фикстура для инициализации класса TokenService."""
    token_service = TokenService(settings=Settings())
    yield token_service


@pytest.fixture
def mock_jwt_payload() -> dict:
    """Фикстура jwt_payload."""
    jwt_payload = {
        "sub": "26",
        "username": "kapral_ae",
        "email": "aa@mm.com",
    }
    return jwt_payload
