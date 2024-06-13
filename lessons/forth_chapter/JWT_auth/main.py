from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from models.models import User
from datetime import datetime, timedelta, UTC


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Секретный ключ для подписи и верификации токенов JWT
SECRET_KEY = 'mysecretkey'  # в реальной практике используется команда Bash 'openssl rand -hex 32'
ALGORITHM = 'HS256'  # плюс в реальной жизни мы устанавливаем "время жизни" токена

USER_DATA = [
    {'username': 'admin',
     'password': 'adminpass'}
]


# Функция для создания JWT токена
def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# Функция получения User'а по токену
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass


# Функция для получения пользовательских данных на основе имени пользователя
def get_user(username: str):
    for user in USER_DATA:
        if user.get('username') == username:
            return user
    return None


# примерный роут для аутентификации
@app.post('/login')
async def login(user_in: User):
    for user in USER_DATA:
        if user.get('username') == user_in.username and user.get('password') == user_in.password:
            return {'access_token': create_jwt_token({'sub': user_in.username}),
                    'token_type': 'bearer'}
    return {'error': 'Invalid credentials'}


# защищенный роут для получения информации о пользователе
@app.get('/about_me')
async def about_me(current_user: str = Depends(get_user_from_token)):
    user = get_user(current_user)
    if user:
        return user
    return {'error': 'User not found'}
