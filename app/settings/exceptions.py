from fastapi import HTTPException
from starlette import status


class DoNotExistCertDirError(HTTPException):
    """Исключение, указывающие, что отсутствует директория сертификатов, на основании которых происходит шифрование."""

    def __init__(self, detail: str = "Do not exist ./app/cert dir."):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail
        super().__init__(
                status_code=self.status_code,
                detail=self.detail
        )


class FileCertNotFoundError(HTTPException):
    """Исключение указывает, что не сгенерированы public/private ключи."""

    def __init__(self, detail: str = "Do not exist public/private certs."):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail
        super().__init__(
                status_code=self.status_code,
                detail=self.detail
        )
