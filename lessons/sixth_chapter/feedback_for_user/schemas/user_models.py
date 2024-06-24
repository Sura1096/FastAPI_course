from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    password: constr(min_length=8, max_length=16)
