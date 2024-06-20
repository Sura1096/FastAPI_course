from pydantic import BaseModel


class ResponseModel(BaseModel):
    age: int


class User(BaseModel):
    username: str
