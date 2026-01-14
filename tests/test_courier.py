import allure
import pytest
import requests
import sys
import os

# Добавляем родительскую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helper import BASE_URL, generate_random_string, register_new_courier_and_return_login_password, login_courier

class TestCreateCourier:
    @allure.title("Тест на успешное создание курьера")
    def test_create_courier_success(self):
        """Проверка успешного создания курьера"""
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_response = login_courier(payload["login"], payload["password"])
        if login_response.status_code == 200:
            courier_id = login_response.json()['id']
            requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')

    @allure.title("Тест на создание дубликата курьера")
    def test_create_duplicate_courier_fails(self, create_courier):
        """Проверка, что нельзя создать двух одинаковых курьеров"""
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": courier_data[1],
            "firstName": courier_data[2]
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

    @allure.title("Тест на создание курьера без обязательных полей")
    @pytest.mark.parametrize('missing_field', ['login', 'password', 'firstName'])
    def test_create_courier_missing_field_fails(self, missing_field):
        """Проверка создания курьера без обязательных полей"""
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        del payload[missing_field]
        
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

class TestLoginCourier:
    @allure.title("Тест на успешную авторизацию курьера")
    def test_login_courier_success(self, create_courier):
        """Проверка успешной авторизации курьера"""
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
        
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Тест на авторизацию с неверным паролем")
    def test_login_courier_wrong_password_fails(self, create_courier):
        """Проверка авторизации с неверным паролем"""
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": "wrong_password"
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Тест на авторизацию с несуществующим логином")
    def test_login_courier_non_existent_fails(self):
        """Проверка авторизации с несуществующим логином"""
        payload = {
            "login": "nonexistent_user_12345",
            "password": "password123"
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Тест на авторизацию без обязательных полей")
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_courier_missing_field_fails(self, missing_field, create_courier):
        """Проверка авторизации без обязательных полей"""
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        
        del payload[missing_field]
        
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]
