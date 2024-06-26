import unittest
from fastapi.testclient import TestClient
from main import app, get_anime, get_parsed_data
from unittest.mock import patch


client = TestClient(app)


class TestGetAnimeData(unittest.TestCase):
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

    @patch("main.get_anime")
    def test_not_found_anime(self, mock_get_anime):
        mock_get_anime.return_value = None

        error_raised = {
            "detail": "Anime not found"
        }

        response = client.get("/data/2")
        mock_get_anime.assert_called_once()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), error_raised)


class TestCreateAnimeItem(unittest.TestCase):
    @patch("main.get_anime")
    @patch("main.get_parsed_data")
    def test_create_anime_and_parse(self, mock_parse_anime, mock_get_anime):
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

        users_data = {
            "anime_id": 15
        }

        response = client.post("/create/", json=users_data)
        mock_get_anime.assert_called_once()
        mock_parse_anime.assert_called_once_with(mock_response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_parsed_data)

    @patch("main.get_anime")
    @patch("main.get_parsed_data")
    def test_create_anime_that_exists(self, mock_parse_anime, mock_get_anime):
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

        users_data = {
            "anime_id": 15
        }

        error_raised = {
            "detail": "Anime already exists"
        }

        response = client.post("/create/", json=users_data)
        mock_get_anime.assert_called_once()
        mock_parse_anime.assert_called_once_with(mock_response)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), error_raised)

    @patch("main.get_anime")
    def test_create_anime_not_found(self, mock_get_anime):
        mock_get_anime.return_value = None

        users_data = {
            "anime_id": 2
        }

        error_raised = {
            "detail": "Anime not found"
        }

        response = client.post("/create/", json=users_data)
        mock_get_anime.assert_called_once()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), error_raised)
