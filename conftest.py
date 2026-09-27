import pytest
import requests
import uuid
from urls import REGISTER_URL, INGREDIENTS_URL



@pytest.fixture(scope="module")
def registered_user():
    """Фикстура для регистрации пользователя и получения токенов"""
    random_id = str(uuid.uuid4())[:8]
    user_data = {
        "email": f"test_{random_id}@ya.ru",
        "password": "testpassword123",
        "name": f"Test User {random_id}"
    }
    response = requests.post(REGISTER_URL, json=user_data)

    assert response.status_code == 200, f"Failed to register user: {response.text}"
    data = response.json()
    assert data["success"] is True
    return {
        "user": user_data,
        "access_token": data["accessToken"],
        "refresh_token": data["refreshToken"]
    }


@pytest.fixture(scope="module")
def ingredient_ids():
    """Фикстура для получения списка валидных ID ингредиентов"""
    response = requests.get(INGREDIENTS_URL)
    assert response.status_code == 200, f"Failed to get ingredients: {response.text}"
    data = response.json()
    # Берем первые два ингредиента для тестов
    return [data["data"][0]["_id"], data["data"][1]["_id"]]


@pytest.fixture(scope="module")
def auth_headers(registered_user):
    """Фикстура для заголовков авторизации"""
    return {
        "Authorization": registered_user["access_token"]
    }