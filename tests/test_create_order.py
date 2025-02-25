import allure

from conftest import create_and_remove_user
from constants import USER, EMAIL
from urls import ORDER_URL
from utils import *

DATA = "data"


class TestCreateOrder:

    @allure.title("Проверка создания заказа под авторизованным пользователем")
    def test_authorized_create_order(self, create_and_remove_user):
        user = create_and_remove_user.json().get(USER)
        login_body = {
            "email": user.get(EMAIL),
            "password": PASSWORD
        }
        login_user(login_body)
        ingredient_response = get_ingredients_response()
        ingredients: list = ingredient_response.json().get(DATA)
        ingredient_ids = get_random_ingredient_ids(ingredients, 2)
        order_data = {
            "ingredients": ingredient_ids
        }
        order_response = requests.post(ORDER_URL, headers=CONTENT_HEADER, json=order_data)
        assert order_response.status_code == 200 and order_response.json().get("success") is True

    @allure.title("Проверка создания заказа под неавторизованным пользователем")
    def test_unauthorized_create_order(self):
        ingredient_response = get_ingredients_response()
        ingredients: list = ingredient_response.json().get(DATA)
        ingredient_ids = get_random_ingredient_ids(ingredients, 2)
        order_data = {
            "ingredients": ingredient_ids
        }
        order_response = requests.post(ORDER_URL, headers=CONTENT_HEADER, json=order_data)
        assert order_response.status_code == 200 and order_response.json().get("success") is True

    @allure.title("Проверка создания без ингредиентов")
    def test_create_order_without_ingredients(self):
        order_data = {
            "ingredients": []
        }
        order_response = requests.post(ORDER_URL, headers=CONTENT_HEADER, json=order_data)
        assert order_response.status_code == 400
        assert order_response.json() == {"success": False, "message": "Ingredient ids must be provided"}

    @allure.title("Проверка создания заказа с неправильными ингредиентами")
    def test_create_order_with_wrong_ingredients(self):
        order_data = {
            "ingredients": [
                generate_random_string(9) + '125',
                generate_random_string(9) + '658'
            ]
        }
        order_response = requests.post(ORDER_URL, headers=CONTENT_HEADER, json=order_data)
        assert order_response.status_code == 400
        assert order_response.json() == {"success": False, "message": "One or more ids provided are incorrect"}
