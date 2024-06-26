from fastapi import FastAPI, HTTPException

from jikan_api.jikan_api import JikanAPI
from jikan_api.parse_data_from_api import get_parsed_data

from schemas.schemas import AnimeModel


app = FastAPI()

anime_db: dict = {}


def get_anime(anime_id):
    anime = JikanAPI()
    return anime.get_anime_by_id(anime_id)


@app.post("/create/")
async def create_anime_item(anime_model: AnimeModel):
    data = get_anime(anime_model.anime_id)
    if data:
        anime_data = get_parsed_data(data)
        if anime_data["mal_id"] not in anime_db:
            anime_db.update({anime_data["mal_id"]: anime_data})
            return anime_data
        else:
            raise HTTPException(status_code=409, detail="Anime already exists")
    else:
        raise HTTPException(status_code=404, detail="Anime not found")


@app.get("/data/{anime_id}", response_model=dict)
async def get_anime_data(anime_id: int):
    data = get_anime(anime_id)
    if data:
        return get_parsed_data(data)
    else:
        raise HTTPException(status_code=404, detail="Anime not found")
