import pytest
import requests
import allure
from urls import BASE_URL


@allure.feature("Создание заказа")
@allure.tag("orders", "post")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.description("Проверяет, что авторизованный пользователь может создать заказ с валидными ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, auth_headers, ingredient_ids):
        """Создание заказа с авторизацией и с ингредиентами"""
        with allure.step("Формируем payload со списком валидных ID ингредиентов"):
            payload = {"ingredients": ingredient_ids}

        with allure.step("Отправляем POST-запрос на /orders с заголовком авторизации"):
            response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)

        with allure.step("Проверяем, что статус ответа равен 200"):
            assert response.status_code == 200

        with allure.step("Проверяем, что success=True и в ответе есть order с номером"):
            data = response.json()
            assert data["success"] is True
            assert "order" in data
            assert "number" in data["order"]

    @allure.title("Создание заказа без авторизации (гостевой заказ)")
    @allure.description("Проверяет, что API позволяет создать заказ анонимному пользователю")
    def test_create_order_without_auth(self, ingredient_ids):
        """Создание заказа без авторизации (гостевой заказ)"""
        with allure.step("Формируем payload со списком валидных ID ингредиентов"):
            payload = {"ingredients": ingredient_ids}

        with allure.step("Отправляем POST-запрос на /orders без заголовка авторизации"):
            response = requests.post(f"{BASE_URL}/orders", json=payload)

        with allure.step("Проверяем, что статус ответа равен 200 (гостевой заказ разрешён)"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"

        with allure.step("Проверяем, что success=True и в ответе есть order с номером"):
            data = response.json()
            assert data["success"] is True
            assert "order" in data
            assert "number" in data["order"]

    @allure.title("Попытка создания заказа без ингредиентов")
    @allure.description("Проверяет, что сервер вернёт ошибку 400 при пустом списке ингредиентов")
    def test_create_order_without_ingredients(self, auth_headers):
        """Создание заказа без ингредиентов"""
        with allure.step("Формируем payload с пустым списком ингредиентов"):
            payload = {"ingredients": []}

        with allure.step("Отправляем POST-запрос на /orders с заголовком авторизации"):
            response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)

        with allure.step("Проверяем, что статус ответа равен 400 Bad Request"):
            assert response.status_code == 400

        with allure.step("Проверяем, что success=False и присутствует сообщение об ошибке"):
            data = response.json()
            assert data["success"] is False
            assert "message" in data

    @allure.title("Попытка создания заказа с невалидным хешем ингредиента")
    @allure.description("Проверяет, что сервер вернёт ошибку 500 при невалидном ID ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self, auth_headers):
        """Создание заказа с неверным хешем ингредиентов"""
        with allure.step("Формируем payload с невалидным хешем ингредиента"):
            payload = {"ingredients": ["invalid_hash_12345"]}

        with allure.step("Отправляем POST-запрос на /orders с заголовком авторизации"):
            response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)

        with allure.step("Проверяем, что статус ответа равен 500 Internal Server Error"):
            assert response.status_code == 500