from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from currency_exchange_API.app.core.security import get_token_by_username, get_user
from ..schemas.user import User
from currency_exchange_API.app.db.db import USER_DATA


auth_user_route = APIRouter(
    prefix='/auth'
)


@auth_user_route.post('/register/')
async def register_user(user: User):
    user_not_exists = get_user(user.username)
    if not user_not_exists:
        USER_DATA.append(user)
        return {'message': f'User {user.username} successfully added!'}
    else:
        raise HTTPException(status_code=409, detail='User with that username already exists.')


@auth_user_route.post('/login/')
async def login(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_get = get_user(user.username)

    if user_get is None or user_get.get('password') != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    token = get_token_by_username(user.username)
    return {'message': token}
