from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models.models import User


USER_DATA = [
    User(**{'username': 'Sura', 'password': 'sura2001'}),
    User(**{'username': 'Saya', 'password': 'saya1999'})
]


app = FastAPI()
security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={"WWW-Authenticate": "Basic"}
        )
    return user


def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


@app.get('/login')
def get_protected_resource(user: User = Depends(authenticate_user)):
    return {
        'message': 'You got my secret, welcome'
    }
