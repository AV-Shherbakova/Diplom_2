import requests

from conftest import create_and_remove_user
from constants import USER, EMAIL, PASSWORD
from urls import ORDER_URL
from utils import login_user, get_content_header, get_ingredients_response, get_random_index_from_list, \
    generate_random_string

DATA = "data"

ID = "_id"


class TestCreateOrder:

    @staticmethod
    def get_random_ingredient_ids(ingredients: list, quantity: int):
        ingredient_ids = []
        for i in range(quantity):
            idx = get_random_index_from_list(ingredients)
            ingredient_ids.append(ingredients[idx].get(ID))
        return ingredient_ids

    def test_authorized_create_order(self, create_and_remove_user):
        assert create_and_remove_user.status_code == 200
        user = create_and_remove_user.json().get(USER)
        login_body = {
            "email": user.get(EMAIL),
            "password": PASSWORD
        }
        login_response = login_user(login_body)
        assert login_response.status_code == 200
        self.create_ingredients_order()

    def test_unauthorized_create_order(self):
        self.create_ingredients_order()

    def test_create_order_without_ingredients(self):
        order_data = {
            "ingredients": []
        }
        order_response = requests.post(ORDER_URL, headers=get_content_header(), json=order_data)
        assert order_response.status_code == 400
        assert order_response.json() == {"success": False, "message": "Ingredient ids must be provided"}

    def test_create_order_with_wrong_ingredients(self):
        order_data = {
            "ingredients": [
                generate_random_string(9) + '125',
                generate_random_string(9) + '658'
            ]
        }
        order_response = requests.post(ORDER_URL, headers=get_content_header(), json=order_data)
        assert order_response.status_code == 400
        assert order_response.json() == {"success": False, "message": "One or more ids provided are incorrect"}

    def create_ingredients_order(self):
        ingredient_response = get_ingredients_response()
        assert ingredient_response.status_code == 200
        ingredients: list = ingredient_response.json().get(DATA)
        assert len(ingredients) >= 2
        ingredient_ids = self.get_random_ingredient_ids(ingredients, 2)
        order_data = {
            "ingredients": ingredient_ids
        }
        order_response = requests.post(ORDER_URL, headers=get_content_header(), json=order_data)
        assert order_response.status_code == 200
        assert order_response.json().get("success") is True
