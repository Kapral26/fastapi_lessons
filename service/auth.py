from dataclasses import dataclass

from schemas import UserLoginDTO


@dataclass
class AuthService:
    def login(self, username: str, password: str) -> UserLoginDTO:
        pass
