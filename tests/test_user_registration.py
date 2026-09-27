import pytest
import requests
import uuid
import allure
from urls import REGISTER_URL


# На уровне класса — группировка по фиче
@allure.feature("Регистрация пользователя")
@allure.tag("auth", "register")
class TestUserRegistration:

    @allure.title("Создание уникального пользователя")
    @allure.description("Проверяет, что можно зарегистрировать нового пользователя с уникальным email")
    def test_register_unique_user(self):
        with allure.step("Генерируем уникальные данные"):
            random_id = str(uuid.uuid4())[:8]
            payload = {
                "email": f"unique_{random_id}@ya.ru",
                "password": "testpassword123",
                "name": f"Unique User {random_id}"
            }

        with allure.step("Отправляем POST-запрос на /auth/register"):
            response = requests.post(REGISTER_URL, json=payload)

        with allure.step("Проверяем статус ответа"):
            assert response.status_code == 200

        with allure.step("Проверяем наличие токенов в ответе"):
            data = response.json()
            assert data["success"] is True
            assert "accessToken" in data
            assert "refreshToken" in data

    @allure.title("Попытка создать уже существующего пользователя")
    @allure.description("Проверяет, что сервер вернёт ошибку при повторной регистрации")
    def test_register_existing_user(self, registered_user):
        with allure.step("Формируем payload с данными уже зарегистрированного пользователя"):
            payload = {
                "email": registered_user["user"]["email"],
                "password": registered_user["user"]["password"],
                "name": registered_user["user"]["name"]
            }

        with allure.step("Отправляем POST-запрос"):
            response = requests.post(REGISTER_URL, json=payload)

        with allure.step("Проверяем, что получен 403 или 400"):
            assert response.status_code in [403, 400]

        with allure.step("Проверяем success=false"):
            data = response.json()
            assert data["success"] is False

    @allure.title("Регистрация без обязательного поля")
    @allure.description("Проверяет, что сервер отклонит запрос без поля name")
    def test_register_missing_required_field(self):
        with allure.step("Генерируем уникальный email"):
            random_id = str(uuid.uuid4())[:8]
            payload = {
                "email": f"missing_field_{random_id}@ya.ru",
                "password": "testpassword123"
            }

        with allure.step("Отправляем запрос без поля name"):
            response = requests.post(REGISTER_URL, json=payload)

        with allure.step("Проверяем код ответа"):
            assert response.status_code in [400, 403, 500]

        with allure.step("Проверяем success=false"):
            data = response.json()
            assert data["success"] is False