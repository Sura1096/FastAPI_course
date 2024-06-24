from fastapi.exceptions import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = 'User not found', status_code: int = 404):
        super().__init__(status_code=status_code,
                         detail=detail)


class InvalidUserDataException(HTTPException):
    def __init__(self, detail: str = 'Invalid user data', status_code: int = 422):
        super().__init__(status_code=status_code,
                         detail=detail)
