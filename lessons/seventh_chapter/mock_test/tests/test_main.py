import unittest
from fastapi.testclient import TestClient
from main import app, get_anime, get_parsed_data
from unittest.mock import patch


client = TestClient(app)


class TestMain(unittest.TestCase):
    @patch("main.get_anime")
    @patch("main.get_parsed_data")
    def test_get_anime_and_parse(self, mock_parse_anime, mock_get_anime):
        mock_response = {
            "data": {
                "mal_id": 15,
                "title": "Eyeshield 21",
                "status": "Finished Airing",
                "score": 7.91
            }
        }
        mock_get_anime.return_value = mock_response

        mock_parsed_data = {
            "mal_id": 15,
            "title": "Eyeshield 21",
            "status": "Finished Airing",
            "score": 7.91
        }
        mock_parse_anime.return_value = mock_parsed_data

        response = client.get("/data/15")
        mock_get_anime.assert_called_once()
        mock_parse_anime.assert_called_once_with(mock_response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_parsed_data)
