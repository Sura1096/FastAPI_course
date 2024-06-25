from fastapi.testclient import TestClient
from fastapi_app import app


client = TestClient(app)


class TestCreateEndpoint:
    def test_create_user_valid(self):
        # Test case 1: валидные входные данные
        user_data = {
            "user_id": 2,
            "username": "Saya",
            "email": "saya.murodova@gmail.com",
            "password": "mentalhealth3"
        }

        response = client.post("/create_user/", json=user_data)

        assert response.status_code == 200
        assert response.json() == {"message": "User was successfully created."}

    def test_create_user_that_already_exists(self):
        # Test case 2: пользователь уже существует
        user_data = {
            "user_id": 2,
            "username": "Saya",
            "email": "saya.murodova@gmail.com",
            "password": "mentalhealth3"
        }

        response = client.post("/create_user/", json=user_data)

        assert response.status_code == 409
        assert response.json() == {"detail": "User already exists"}

    def test_create_user_invalid_data(self):
        # Test case 3: невалидные входные данные
        user_data = {
            "user_id": 1,
            "username": "Sura",
            "email": "sura.murodova@gmail.com",
        }

        response = client.post("/create_user/", json=user_data)

        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": [
                        "body",
                        "password"
                    ],
                    "msg": "Field required",
                    "input": {
                        "user_id": 1,
                        "username": "Sura",
                        "email": "sura.murodova@gmail.com"
                    }
                }
            ]
        }


class TestGetEndpoint:
    def test_get_user_valid(self):
        # Test case 1: валидные входные данные
        response = client.get("/get_user/2")

        assert response.status_code == 200
        assert response.json() == {
            "username": "Saya",
            "email": "saya.murodova@gmail.com",
            "password": "mentalhealth3"
        }

    def test_get_user_not_found(self):
        # Test case 2: невалидные входные данные
        response = client.get("/get_user/4")

        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}


class TestDeleteEndpoint:
    def test_delete_user_valid(self):
        # Test case 1: валидные входные данные
        response = client.delete("/del_user/2")

        assert response.status_code == 200
        assert response.json() == {"message": "User was successfully deleted."}

    def test_delete_not_existing_user(self):
        # Test case 2: невалидные входные данные
        response = client.delete("/del_user/5")

        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
