import pytest
import requests
from urls import BASE_URL


class TestGetOrders:
    def test_get_orders_with_auth(self, auth_headers):
        """Получение заказов конкретного пользователя (авторизованный)"""
        response = requests.get(f"{BASE_URL}/orders", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "orders" in data

    def test_get_orders_without_auth(self):
        """Получение заказов конкретного пользователя (неавторизованный)"""
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "message" in data