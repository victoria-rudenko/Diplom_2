import pytest
import requests
import allure
from urls import BASE_URL


@allure.feature("Получение заказов пользователя")
@allure.tag("orders", "get")
class TestGetOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    @allure.description("Проверяет, что авторизованный пользователь может получить список своих заказов")
    def test_get_orders_with_auth(self, auth_headers):
        """Получение заказов конкретного пользователя (авторизованный)"""
        with allure.step("Отправляем GET-запрос на /orders с заголовком авторизации"):
            response = requests.get(f"{BASE_URL}/orders", headers=auth_headers)

        with allure.step("Проверяем, что статус ответа равен 200"):
            assert response.status_code == 200

        with allure.step("Проверяем, что success=True и в ответе присутствует поле 'orders'"):
            data = response.json()
            assert data["success"] is True
            assert "orders" in data

    @allure.title("Попытка получения заказов без авторизации")
    @allure.description("Проверяет, что сервер вернёт ошибку 401 при запросе без токена")
    def test_get_orders_without_auth(self):
        """Получение заказов конкретного пользователя (неавторизованный)"""
        with allure.step("Отправляем GET-запрос на /orders без заголовка авторизации"):
            response = requests.get(f"{BASE_URL}/orders")

        with allure.step("Проверяем, что статус ответа равен 401 Unauthorized"):
            assert response.status_code == 401

        with allure.step("Проверяем, что success=False и присутствует сообщение об ошибке"):
            data = response.json()
            assert data["success"] is False
            assert "message" in data