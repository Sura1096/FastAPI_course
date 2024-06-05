from fastapi import FastAPI, Response, Cookie
from models.models import User


app = FastAPI()

# имитируем хранилище юзеров
sample_user: dict = {'username': 'Sura', 'password': 'qwerty'}  # создали тестового юзера, якобы он уже зарегистрирован у нас
fake_db: list[User] = [User(**sample_user)]  # имитируем базу данных

# имитируем хранилище сессий
session: dict = {}  # это можно хранить в кэше, например в Redis


@app.post('/login')
async def login(user: User, response: Response):
    for person in fake_db:
        if person.username == user.username and person.password == user.password:
            session_token = 'abc123xyz456'
            session[session_token] = user

            # тут установили куки с защищенным флагом httponly - недоступны для вредоносного JS
            response.set_cookie(key='session_token', value=session_token, httponly=True)
            return {'message': 'cookie are set'}

    return {'message': 'Invalid username or password'}


@app.get('/user')
async def user_info(session_token=Cookie()):
    user = session.get(session_token)

    if user:
        return user.dict()
    return {'message': 'Unauthorized'}
