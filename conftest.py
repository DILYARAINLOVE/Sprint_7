import pytest
import requests
from helper import register_new_courier_and_return_login_password, login_courier, delete_courier, BASE_URL

@pytest.fixture
def create_courier():
    """Фикстура для создания курьера"""
    courier_data = register_new_courier_and_return_login_password()
    yield courier_data
    # После теста удаляем курьера
    if courier_data:
        login_response = login_courier(courier_data[0], courier_data[1])
        if login_response.status_code == 200:
            courier_id = login_response.json()['id']
            delete_courier(courier_id)

@pytest.fixture
def get_order_data():
    """Фикстура для данных заказа"""
    return {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "ул. Пушкина, д. 1",
        "metroStation": 4,
        "phone": "+79999999999",
        "rentTime": 5,
        "deliveryDate": "2024-12-31",
        "comment": "Тестовый заказ"
    }