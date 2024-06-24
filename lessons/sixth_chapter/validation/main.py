from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from models.models import User
from fastapi.responses import JSONResponse


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def custom_req_validation_error_handler(req: Request, exc: RequestValidationError):
    errors = [error.get('msg') for error in exc.errors()]
    return JSONResponse(
        status_code=400,
        content={'errors': errors}
    )


@app.get('/users')
async def example(user: User):
    return user
