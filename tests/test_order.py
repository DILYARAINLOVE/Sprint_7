import allure
import pytest
import requests
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
        
        # Добавляем цвет к данным заказа
        if color:
            order_data["color"] = color
        
        response = requests.post(f'{BASE_URL}/api/v1/orders', json=order_data)
        
        # Проверяем код ответа
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
        
        # Проверяем, что в ответе есть номер трека
        assert "track" in response.json(), "В ответе отсутствует поле 'track'"
        
        # Проверяем, что track является числом
        track_number = response.json()["track"]
        assert isinstance(track_number, int), "Track должен быть числом"
        
        # Дополнительно можно проверить, что трек положительный
        assert track_number > 0, "Track должен быть положительным числом"

    @allure.title("Тест на создание заказа без указания цвета")
    def test_create_order_without_color(self, get_order_data):
        """Проверка создания заказа без указания цвета"""
        order_data = get_order_data
        # Не добавляем поле color
        
        response = requests.post(f'{BASE_URL}/api/v1/orders', json=order_data)
        
        # Проверяем код ответа
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
        
        # Проверяем, что в ответе есть номер трека
        assert "track" in response.json(), "В ответе отсутствует поле 'track'"

class TestGetOrdersList:
    @allure.title("Тест на получение списка заказов")
    def test_get_orders_list(self):
        """Проверка получения списка заказов"""
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        
        # Проверяем код ответа
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        
        # Проверяем, что в ответе есть список заказов
        assert "orders" in response.json(), "В ответе отсутствует поле 'orders'"
        
        orders = response.json()["orders"]
        
        # Проверяем, что orders является списком
        assert isinstance(orders, list), "Orders должен быть списком"
        
        # Если список не пустой, проверяем структуру первого элемента
        if orders:
            order = orders[0]
            # Проверяем обязательные поля в заказе
            assert "id" in order, "В заказе отсутствует поле 'id'"
            assert "track" in order, "В заказе отсутствует поле 'track'"