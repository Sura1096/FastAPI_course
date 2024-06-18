from pydantic import BaseModel


class ToDoCreate(BaseModel):
    title: str
    description: str


class ToDoUpdate(BaseModel):
    title: str
    description: str
    completed: bool = False


class ToDoReturn(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
