from fastapi import FastAPI
from models.models import UserID, UserAge


app = FastAPI()


my_user: UserID = UserID(name='Sura', id=6)


@app.get('/users')
def get_user():
    return {'name': my_user.name, 'id': my_user.id}


@app.post('/user')
async def is_adult(user_data: UserAge):
    return {'name': user_data.name,
            'age': user_data.age,
            'is_adult': user_data.age >= 18}