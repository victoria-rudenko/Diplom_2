import pytest
import requests
import allure
from urls import BASE_URL


@allure.feature("Авторизация пользователя")
@allure.tag("auth", "login")
class TestUserLogin:

    @allure.title("Успешная авторизация существующего пользователя")
    @allure.description("Проверяет, что пользователь может войти в систему с корректными учётными данными")
    def test_login_existing_user(self, registered_user):
        """Логин под существующим пользователем"""
        with allure.step("Формируем payload с email и паролем зарегистрированного пользователя"):
            payload = {
                "email": registered_user["user"]["email"],
                "password": registered_user["user"]["password"]
            }

        with allure.step("Отправляем POST-запрос на /auth/login"):
            response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        with allure.step("Проверяем, что статус ответа равен 200"):
            assert response.status_code == 200

        with allure.step("Проверяем, что success=True и в ответе присутствуют accessToken и refreshToken"):
            data = response.json()
            assert data["success"] is True
            assert "accessToken" in data
            assert "refreshToken" in data

    @allure.title("Попытка авторизации с неверными учётными данными")
    @allure.description("Проверяет, что сервер вернёт ошибку 401 при неверном email или пароле")
    def test_login_invalid_credentials(self):
        """Логин с неверным логином и паролем"""
        with allure.step("Формируем payload с несуществующим email и неверным паролем"):
            payload = {
                "email": "wrong_email@ya.ru",
                "password": "wrong_password"
            }

        with allure.step("Отправляем POST-запрос на /auth/login"):
            response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        with allure.step("Проверяем, что статус ответа равен 401 Unauthorized"):
            assert response.status_code == 401

        with allure.step("Проверяем, что success=False и присутствует сообщение об ошибке"):
            data = response.json()
            assert data["success"] is False
            assert "message" in data