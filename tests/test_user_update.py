import pytest
import requests
import uuid
import allure
from urls import AUTH_USER_URL


@allure.feature("Изменение данных пользователя")
@allure.tag("auth", "user", "patch")
class TestUserUpdate:

    @allure.title("Успешное изменение данных пользователя с авторизацией")
    @allure.description("Проверяет, что авторизованный пользователь может обновить свои имя и email")
    def test_update_user_with_auth(self, registered_user):
        """Изменение данных пользователя с авторизацией"""
        with allure.step("Генерируем уникальные значения для новых email и name"):
            random_id = str(uuid.uuid4())[:8]
            new_email = f"updated_{random_id}@ya.ru"
            new_name = f"Updated Name {random_id}"

        with allure.step("Формируем payload с новыми данными пользователя"):
            payload = {
                "name": new_name,
                "email": new_email
            }

        with allure.step("Формируем заголовки с токеном авторизации"):
            headers = {"Authorization": registered_user["access_token"]}

        with allure.step("Отправляем PATCH-запрос на /auth/user"):
            response = requests.patch(AUTH_USER_URL, json=payload, headers=headers)

        with allure.step("Проверяем, что статус ответа равен 200"):
            assert response.status_code == 200

        with allure.step("Проверяем, что success=True и данные пользователя обновлены"):
            data = response.json()
            assert data["success"] is True
            assert data["user"]["name"] == new_name
            assert data["user"]["email"] == new_email

        with allure.step("Обновляем данные в фикстуре для последующих тестов"):
            registered_user["user"]["name"] = new_name
            registered_user["user"]["email"] = new_email

    @allure.title("Попытка изменения данных без авторизации")
    @allure.description("Проверяет, что сервер вернёт ошибку 401 при запросе без токена")
    def test_update_user_without_auth(self, registered_user):
        """Изменение данных пользователя без авторизации (должна быть ошибка)"""
        with allure.step("Формируем payload с новыми данными пользователя"):
            payload = {"name": "Hacker Name"}

        with allure.step("Отправляем PATCH-запрос на /auth/user без заголовка авторизации"):
            response = requests.patch(AUTH_USER_URL, json=payload)

        with allure.step("Проверяем, что статус ответа равен 401 Unauthorized"):
            assert response.status_code == 401

        with allure.step("Проверяем, что success=False и присутствует сообщение об ошибке"):
            data = response.json()
            assert data["success"] is False
            assert "message" in data