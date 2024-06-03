from fastapi import FastAPI
from models.models import Feedback


app = FastAPI()


fake_users = {
    1: {'username': 'Sura', 'email': 'suri.murodova@gmail.com'},
    2: {'username': 'Saya', 'email': 'saya.murodova@gmail.com'}
}


fake_feedback = []


@app.get('/users/')
async def read_user(limit: int = 10):
    return dict(list(fake_users.items())[:limit])


@app.post('/feedback')
async def save_feedback(feedback: Feedback):
    fake_feedback.append({'name': feedback.name, 'message': feedback.message})
    return {'message': f'Feedback received. Thank you, {feedback.name}!'}
