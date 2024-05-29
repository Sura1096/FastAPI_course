from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI()


class Numbers(BaseModel):
    num1: int
    num2: int


@app.get('/')
async def root():
    return FileResponse('index.html')


@app.post('/calculate/')
async def calculate_sum(nums: Numbers):
    result = nums.num1 + nums.num2
    return {'result': result}
