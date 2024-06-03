from pydantic import BaseModel


class UserID(BaseModel):
    name: str
    id: int


class UserAge(BaseModel):
    name: str
    age: int
