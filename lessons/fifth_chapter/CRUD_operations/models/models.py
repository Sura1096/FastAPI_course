from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str


class UserReturn(BaseModel):
    username: str
    email: str
    id: Optional[int] = None
