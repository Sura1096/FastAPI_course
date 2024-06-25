from fastapi.exceptions import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = 'User not found', status_code: int = 404):
        super().__init__(status_code=status_code,
                         detail=detail)


class ConflictException(HTTPException):
    def __init__(self, detail: str = 'User already exists', status_code: int = 409):
        super().__init__(status_code=status_code,
                         detail=detail)
