from fastapi import FastAPI, Header, HTTPException
from typing import Annotated


app = FastAPI()


@app.get('/headers')
async def get_headers(
        user_agent: Annotated[str | None, Header()] = None,
        accept_language: Annotated[str | None, Header()] = None
):
    if not user_agent or not accept_language:
        raise HTTPException(
            status_code=400,
            detail='Required headers to complete this request are missing')
    return {'User-Agent': user_agent,
            'Accept-Language': accept_language}
