from pydantic import BaseModel, ConfigDict


class ToDoCreate(BaseModel):
    title: str
    description: str
    completed: bool | None = False


class ToDoFromDB(ToDoCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

