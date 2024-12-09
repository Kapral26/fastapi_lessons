from dataclasses import dataclass
from datetime import timedelta, datetime, timezone

from jose import jwt

from app.settings.main_settings import Settings


@dataclass
class TokenService:
    settings: Settings

    def create_jwt(
            self,
            token_type: str,
            token_data: dict,
            expire_minutes: int | None = None,
            expire_timedelta: timedelta | None = None
    ) -> str:
        """
        Создает JWT-токен.

        :param token_type: Тип токена.
        :param token_data: Данные для включения в токен.
        :param expire_minutes: Количество минут до истечения срока действия токена. По умолчанию берется из настроек.
        :param expire_timedelta: Необязательный параметр. Продолжительность срока действия токена в виде объекта timedelta.
        :return: Сгенерированный JWT-токен.
        """
        expire_minutes = expire_minutes or self.settings.auth_jwt.access_token_expire_minutes

        jwt_payload = {
            self.settings.auth_jwt.access_token_field: token_type,
        }
        jwt_payload.update(token_data)
        return self.encode_jwt(
                payload=jwt_payload,
                expire_minutes=expire_minutes,
                expire_timedelta=expire_timedelta
        )

    def encode_jwt(
            self,
            payload: dict,
            private_key: str | None = None,
            algorithm: str | None = None,
            expire_minutes: int | None = None,
            expire_timedelta: timedelta | None = None
    ) -> str:
        """
        Создает JWT-токен на основе переданных данных.

        :param payload: Данные для кодирования в токен.
        :param private_key: Приватный ключ для подписи токена.
        :param algorithm: Алгоритм шифрования (по умолчанию задается в настройках).
        :param expire_minutes: Время жизни токена в минутах (по умолчанию из настроек).
        :param expire_timedelta: Объект timedelta для задания времени жизни токена.
                                 Если не указан, используется `expire_minutes`.
        :return: Закодированный JWT-токен.
        """
        private_key = private_key or self.settings.auth_jwt.private_key_path.read_text()
        algorithm = algorithm or self.settings.auth_jwt.algorithm
        expire_minutes = expire_minutes or self.settings.auth_jwt.access_token_expire_minutes

        to_encode = payload.copy()
        expire_timedelta = expire_timedelta if expire_timedelta else timedelta(minutes=expire_minutes)
        now = datetime.now(timezone.utc)
        to_encode.update(
                exp=now + expire_timedelta,
                iat=now
        )
        encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
        return encoded

    def decode_jwt(
            self,
            token: str | bytes,
            public_key: str | None = None,
            algorithm: str | None = None
    ) -> dict:
        """
        Декодирует JWT-токен.

        :param token: JWT-токен в виде строки или байтов.
        :param public_key: Публичный ключ для проверки подписи токена.
        :param algorithm: Алгоритм шифрования (по умолчанию задается в настройках).
        :return: Раскодированные данные токена.
        :raises jwt.exceptions.InvalidTokenError: Если токен недействителен.
        """
        public_key = public_key or self.settings.auth_jwt.public_key_path.read_text()
        algorithm = algorithm or self.settings.auth_jwt.algorithm
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        return decoded

