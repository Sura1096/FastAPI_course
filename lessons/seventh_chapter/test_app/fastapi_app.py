from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from schemas.user_schemas import User
from schemas.exception_schemas import ErrorResponseModel

from exceptions.exceptions import UserNotFoundException, ConflictException


app = FastAPI()

users_db: dict = {}


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail},
        headers={"X-Error": "UserNotFoundException error"}
    )


@app.exception_handler(ConflictException)
async def invalid_user_data_exception_handler(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={"X-Error": "ConflictException error"}
    )


@app.post("/create_user")
async def create_user(user: User):
    if user.user_id in users_db:
        raise ConflictException("User already exists", 409)
    users_db[user.user_id] = {"username": user.username,
                              "password": user.password,
                              "email": user.email}
    return {"message": "User was successfully created."}


@app.get("/get_user/{user_id}")
async def get_users(user_id: int):
    if user_id not in users_db:
        raise UserNotFoundException("User not found", 404)
    return users_db[user_id]


@app.delete("/del_user/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise UserNotFoundException("User not found", 404)
    del users_db[user_id]
    return {"message": "User was successfully deleted."}

