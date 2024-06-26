from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, UTC


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Секретный ключ для подписи и верификации токенов JWT
SECRET_KEY = 'mysecretkey'  # в реальной практике используется команда Bash 'openssl rand -hex 32'
ALGORITHM = 'HS256'

# Переменные для установки срока действия токена
TIME_NOW = datetime.now(UTC)
TOKEN_EXP_MIN = 10

# Пример информации из БД
USER_DATA = [
    {'username': 'admin',
     'password': 'adminpass'}
]


# Фукнция для проверки "username" и "password" по базе данных пользователя
def authenticate_user(username: str, password: str) -> bool:
    for user in USER_DATA:
        if username == user.get('username') and password == user.get('password'):
            return True
    return False


# Функция для создания JWT токена
def create_jwt_token(data: dict):
    payload = data.copy()
    expiration_time = TIME_NOW + timedelta(minutes=TOKEN_EXP_MIN)

    payload.update({'iat': TIME_NOW, 'exp': expiration_time})

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM)
    return token


# Функция получения User'а по токену
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access Token has expired or expiration date is invalid!',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={'WWW-Authenticate': 'Bearer'},
        )


# Функция для получения пользовательских данных на основе имени пользователя
def get_user(username: str):
    for user in USER_DATA:
        if user.get('username') == username:
            return user
    return None
