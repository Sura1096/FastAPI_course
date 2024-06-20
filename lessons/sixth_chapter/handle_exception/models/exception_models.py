from pydantic import BaseModel


class CustomModelA(BaseModel):
    status_code: int
    er_detail: str


class CustomModelB(BaseModel):
    status_code: int
    er_detail: str
