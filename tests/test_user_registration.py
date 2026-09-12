import pytest
import requests
import uuid
from urls import BASE_URL


class TestUserRegistration:
    def test_register_unique_user(self):
        """Создать уникального пользователя"""
        random_id = str(uuid.uuid4())[:8]
        payload = {
            "email": f"unique_{random_id}@ya.ru",
            "password": "testpassword123",
            "name": f"Unique User {random_id}"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data
        assert "refreshToken" in data

    def test_register_existing_user(self, registered_user):
        """Создать пользователя, который уже зарегистрирован"""
        payload = {
            "email": registered_user["user"]["email"],
            "password": registered_user["user"]["password"],
            "name": registered_user["user"]["name"]
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code in [403, 400]
        data = response.json()
        assert data["success"] is False

    def test_register_missing_required_field(self):
        """Создать пользователя и не заполнить одно из обязательных полей (например, name)"""
        random_id = str(uuid.uuid4())[:8]

        payload = {
            "email": f"missing_field_{random_id}@ya.ru",
            "password": "testpassword123"
            # поле name намеренно отсутствует
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)

        assert response.status_code in [400, 403,
                                        500], f"Unexpected status code: {response.status_code}, Response: {response.text}"

        data = response.json()
        assert data["success"] is False