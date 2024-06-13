from fastapi import FastAPI, Depends, HTTPException
from models.models import User
from dependencies.jwt import create_jwt_token, get_user, get_user_from_token


app = FastAPI()
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
            status_code=401,
            detail='Access Token has expired or expiration date is invalid!',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={'WWW-Authenticate': 'Bearer'},
        )


# Функция для получения пользовательских данных на основе имени пользователя
def get_user(username: str):
    for user in USER_DATA:
        if user.get('username') == username:
            return user
    return None


# примерный роут для аутентификации
@app.post('/login')
async def login(user: User):
    user_get = get_user(user.username)

    if user_get.get('password') != user.password:
        raise HTTPException(
            status_code=401,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return {
            'access_token': create_jwt_token(
                {'sub': user.username}
            ),
        }


# защищенный роут для получения информации о пользователе
@app.get('/protected_resource')
async def authenticate_user(cur_user: str = Depends(get_user_from_token)):
    user = get_user(cur_user)

    if not user:
        raise HTTPException(
            status_code=401,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user
