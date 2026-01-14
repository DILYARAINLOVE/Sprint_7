import allure
import pytest
import requests
import sys
import os

# Добавляем родительскую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helper import BASE_URL

class TestCreateOrder:
    @allure.title("Тест на создание заказа с разными цветами")
    @pytest.mark.parametrize('color', [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color, get_order_data):
        """Проверка создания заказа с разными цветами"""
        order_data = get_order_data
        
        if color:
            order_data["color"] = color
        
        response = requests.post(f'{BASE_URL}/api/v1/orders', json=order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Тест на создание заказа без указания цвета")
    def test_create_order_without_color(self, get_order_data):
        """Проверка создания заказа без указания цвета"""
        order_data = get_order_data
        
        response = requests.post(f'{BASE_URL}/api/v1/orders', json=order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()

class TestGetOrdersList:
    @allure.title("Тест на получение списка заказов")
    def test_get_orders_list(self):
        """Проверка получения списка заказов"""
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        
        assert response.status_code == 200
        assert "orders" in response.json()
        
        orders = response.json()["orders"]
        assert isinstance(orders, list)
        
        if orders:
            order = orders[0]
            assert "id" in order
            assert "track" in order
