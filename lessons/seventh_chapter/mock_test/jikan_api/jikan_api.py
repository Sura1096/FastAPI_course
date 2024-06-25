import requests
from typing import Dict, Any


class JikanAPI:
    def __init__(self):
        self.base_url = "https://api.jikan.moe/v4"

    def get_anime_by_id(
            self,
            anime_id: int
    ) -> Dict[str, Any] | None:
        """
        Retrieve details of an anime by its ID.

        Args:
            anime_id (int): The ID of the anime to retrieve.

        Returns:
            dict: A dictionary containing the anime details if found.
            str: 'Not found' if the anime is not found or the request fails.

        Examples:
            anime.get_anime_by_id(5)
        """
        res = requests.get(f'{self.base_url}/anime/{anime_id}')
        if res.status_code != 200:
            return None
        return res.json()
