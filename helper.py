import requests
import random
import string

BASE_URL = 'https://qa-scooter.praktikum-services.ru'

def generate_random_string(length):
    """Генерирует случайную строку из строчных букв"""
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера и возвращает его данные"""
    login_pass = []
    
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    
    return login_pass

def login_courier(login, password):
    """Авторизует курьера и возвращает ответ"""
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    return response

def delete_courier(courier_id):
    """Удаляет курьера по ID"""
    response = requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    return response