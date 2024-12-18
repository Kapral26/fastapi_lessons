"""Тестирование работы с JWT/"""

import pytest

from app.users.auth.exceptions import InvalidAuthTokenError
from app.users.auth.token.service import TokenService


def test_create_jwt(mock_token_service: TokenService, mock_jwt_payload: dict) -> None:
    """Тестирование обертки создание jwt"""
    test_jwt_token = mock_token_service.create_jwt(
            "access", mock_jwt_payload
    )

    assert isinstance(test_jwt_token, str), "Token should be a string"
    assert test_jwt_token, "Token should not be empty"


def test_decode_jwt(mock_token_service: TokenService, mock_jwt_payload: dict) -> None:
    """Тестирование декодирования jwt."""
    encoded_token = mock_token_service.create_jwt(
            "access", mock_jwt_payload
    )

    decoded_result = mock_token_service.decode_jwt(encoded_token)

    for key in mock_jwt_payload:
        assert key in decoded_result, f"Key '{key}' is missing in the decoded result"

    filtered_result = {k: decoded_result[k] for k in mock_jwt_payload}
    assert filtered_result == mock_jwt_payload


def test_encode_jwt(mock_token_service: TokenService, mock_jwt_payload: dict) -> None:
    """Тестирование создание jwt"""
    encoded_jwt = mock_token_service.encode_jwt(mock_jwt_payload)
    assert encoded_jwt, "JWT should not be empty"
    assert isinstance(encoded_jwt, str), "JWT should not be empty"


@pytest.mark.parametrize(
        "payload, token_type, should_raise",
        [
            ({"type": "access"}, "access", False),
            ({"type": "refresh"}, "refresh", False),
            ({"type": "access"}, "refresh", True),
            ({}, "refresh", True),
        ]
)
def test_validate_token_type(
        payload: dict,
        token_type: str,
        should_raise: bool,
        mock_token_service: TokenService
) -> None:
    """Тестирование валидации типа jwt."""
    if should_raise:
        with pytest.raises(InvalidAuthTokenError):
            mock_token_service.validate_token_type(payload, token_type)
    else:
        mock_token_service.validate_token_type(payload, token_type)
