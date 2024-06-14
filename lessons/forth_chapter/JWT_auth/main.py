from fastapi import FastAPI, Depends, HTTPException, status
from models.models import User
from dependencies.jwt import create_jwt_token, get_user, get_user_from_token


app = FastAPI()


# примерный роут для аутентификации
@app.post('/login')
async def login(user: User):
    user_get = get_user(user.username)

    if user_get.get('password') != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user
