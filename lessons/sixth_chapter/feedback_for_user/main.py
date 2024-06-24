from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from schemas.user_models import User
from schemas.exception_models import ErrorResponseModel
from exceptions.exceptions import UserNotFoundException, InvalidUserDataException


app = FastAPI()
users_db = {}


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail},
        headers={"X-Error": "UserNotFoundException error"}
    )


@app.exception_handler(InvalidUserDataException)
async def invalid_user_data_exception_handler(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail},
        headers={"X-Error": "InvalidUserDataException error"}
    )


@app.post('/create_user')
async def create_user(user: User):
    if user.user_id > 100:
        raise InvalidUserDataException('Sorry, your id cannot be greater than 100', 400)
    users_db[user.user_id] = {"username": user.username,
                              "password": user.password,
                              "email": user.email}
    return {'message': 'User was successfully created.'}


@app.get('/get_user/{user_id}')
async def get_users(user_id: int):
    if user_id not in users_db:
        raise UserNotFoundException('User not found')
    return users_db[user_id]
