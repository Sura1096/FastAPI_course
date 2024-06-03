from fastapi import FastAPI
from models.models import Variables


app = FastAPI()


@app.post('/calculate')
def calculate_sum(nums: Variables):
    return {'result': nums.num1 + nums.num2}
