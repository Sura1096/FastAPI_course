from fastapi import FastAPI
from models.models import User


app = FastAPI()


data = {
    'id': 1,
    'name': 'Sura'
}

user = User(**data)


@app.get('/')
async def root():
    return {'message': 'Hello, World!'}


@app.get('/users')
async def get_users():
    return {'users': user}
