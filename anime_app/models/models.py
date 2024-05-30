from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class AnotherUser(BaseModel):
    name: str
    age: int
