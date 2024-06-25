from typing import Any


def get_parsed_data(anime: dict[str, Any]) -> dict[str, Any]:
    anime_data: dict = {}

    anime = anime["data"]
    anime_data["mal_id"] = anime["mal_id"]
    anime_data["title"] = anime["title"]
    anime_data["status"] = anime["status"]
    anime_data["score"] = anime["score"]

    return anime_data
