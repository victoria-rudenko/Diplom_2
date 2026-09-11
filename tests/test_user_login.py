import requests
from urls import BASE_URL


class TestUserLogin:
    def test_login_existing_user(self, registered_user):
        """Логин под существующим пользователем"""
        payload = {
            "email": registered_user["user"]["email"],
            "password": registered_user["user"]["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data
        assert "refreshToken" in data

    def test_login_invalid_credentials(self):
        """Логин с неверным логином и паролем"""
        payload = {
            "email": "wrong_email@ya.ru",
            "password": "wrong_password"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "message" in data
