from fastapi import FastAPI
from models.models import UserCreate


app = FastAPI()


@app.post('/create_user')
async def create_user(user: UserCreate):
    return user
