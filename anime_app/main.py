from fastapi import FastAPI
from models.models import User, AnotherUser


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


@app.post('/user')
async def is_adult(user_data: AnotherUser):
    return {'name': user_data.name,
            'age': user_data.age,
            'is_adult': user_data.age >= 18}
