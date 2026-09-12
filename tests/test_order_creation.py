import pytest
import requests
from urls import BASE_URL

class TestOrderCreation:
    def test_create_order_with_auth_and_ingredients(self, auth_headers, ingredient_ids):
        """Создание заказа с авторизацией и с ингредиентами"""
        payload = {"ingredients": ingredient_ids}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "order" in data
        assert "number" in data["order"]

    def test_create_order_without_auth(self, ingredient_ids):
        """Создание заказа без авторизации (гостевой заказ)"""
        payload = {"ingredients": ingredient_ids}
        response = requests.post(f"{BASE_URL}/orders", json=payload)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"

        data = response.json()
        assert data["success"] is True
        assert "order" in data
        assert "number" in data["order"]

    def test_create_order_without_ingredients(self, auth_headers):
        """Создание заказа без ингредиентов"""
        payload = {"ingredients": []}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "message" in data

    def test_create_order_with_invalid_ingredient_hash(self, auth_headers):
        """Создание заказа с неверным хешем ингредиентов"""
        payload = {"ingredients": ["invalid_hash_12345"]}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)
        assert response.status_code == 500
