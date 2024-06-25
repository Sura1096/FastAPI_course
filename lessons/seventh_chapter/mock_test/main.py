from fastapi import FastAPI, HTTPException

from jikan_api.jikan_api import JikanAPI
from jikan_api.parse_data_from_api import get_parsed_data

from schemas.schemas import AnimeModel


app = FastAPI()

anime_db: dict = {}


def get_anime(anime_id):
    anime = JikanAPI()
    return anime.get_anime_by_id(anime_id)


@app.get("/data/{anime_id}", response_model=dict)
async def get_todo(anime_id: int):
    data = get_anime(anime_id)
    if data:
        return get_parsed_data(data)
    else:
        raise HTTPException(status_code=404, detail="Anime not found")
