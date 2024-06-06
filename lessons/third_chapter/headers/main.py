from fastapi import FastAPI, Header, HTTPException


app = FastAPI()


@app.get('/headers')
async def get_headers(
        user_agent: str = Header(),
        accept_language: str = Header()
):
    if not user_agent or not accept_language:
        raise HTTPException(
            status_code=400,
            detail='Required headers to complete this request are missing')
    return {'User-Agent': user_agent,
            'Accept-Language': accept_language}
