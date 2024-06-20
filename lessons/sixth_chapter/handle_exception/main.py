from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from exceptions.exceptions import CustomExceptionA, CustomExceptionB
from models.exception_models import CustomModelA, CustomModelB
from models.models import ResponseModel, User


app = FastAPI()


@app.exception_handler(CustomExceptionA)
async def exception_handler_A(request: Request, exception: CustomExceptionA):
    error = jsonable_encoder(
        CustomModelA(
            status_code=exception.status_code,
            er_detail=exception.detail
        )
    )
    return JSONResponse(
        status_code=exception.status_code,
        content=error
    )


@app.exception_handler(CustomExceptionB)
async def exception_handler_B(request: Request, exception: CustomExceptionB):
    error = jsonable_encoder(
        CustomModelB(
            status_code=exception.status_code,
            er_detail=exception.detail
        )
    )
    return JSONResponse(
        status_code=exception.status_code,
        content=error
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=500,
        content={'error': 'Internal server error'}
    )


@app.get(
    '/condition/{age}',
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Checks your age",
    description='The endpoint returns users age. '
                'If age is greater than 100, en exception with the status code 500 is returned',
    responses={
        status.HTTP_200_OK: {'model': ResponseModel},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': CustomModelA}
    }
)
async def check_condition(age: int):
    if age > 100:
        raise CustomExceptionA(
            detail='The value of the age is large.',
            status_code=500
        )
    return ResponseModel(age=age)


@app.get(
    '/users/',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Checks your name in database",
    description='The endpoint returns the message about user. '
                'If user not found, en exception with the status code 404 is returned',
    responses={
        status.HTTP_200_OK: {'model': User},
        status.HTTP_404_NOT_FOUND: {'model': CustomModelB}
    }
)
async def check_user(user: User):
    db = ('Adam', 'Maria', 'Sasha', 'Alex')
    if user.username not in db:
        raise CustomExceptionB(
            detail='Username not found.',
            status_code=404
        )
    return User(username=user.username)
