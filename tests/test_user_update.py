import pytest
import requests
import uuid
from urls import BASE_URL


class TestUserUpdate:
    def test_update_user_with_auth(self, registered_user):
        """Изменение данных пользователя с авторизацией"""
        random_id = str(uuid.uuid4())[:8]
        new_email = f"updated_{random_id}@ya.ru"
        new_name = f"Updated Name {random_id}"
        payload = {
            "name": new_name,
            "email": new_email
        }
        headers = {"Authorization": registered_user["access_token"]}

        response = requests.patch(f"{BASE_URL}/auth/user", json=payload, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["user"]["name"] == new_name
        assert data["user"]["email"] == new_email

        registered_user["user"]["name"] = new_name
        registered_user["user"]["email"] = new_email

    def test_update_user_without_auth(self, registered_user):
        """Изменение данных пользователя без авторизации (должна быть ошибка)"""
        payload = {"name": "Hacker Name"}
        response = requests.patch(f"{BASE_URL}/auth/user", json=payload)
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "message" in data