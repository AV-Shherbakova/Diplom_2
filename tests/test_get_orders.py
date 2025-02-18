import requests

from conftest import create_and_remove_user
from constants import ACCESS_TOKEN, EXPECTED_AUTH_ERROR_BODY
from urls import ORDER_URL
from utils import get_auth_header


class TestGetOrders:

    def test_get_orders_authorized(self, create_and_remove_user):
        token = create_and_remove_user.json().get(ACCESS_TOKEN)
        orders_response = requests.get(ORDER_URL, headers=get_auth_header(token))
        assert orders_response.status_code == 200

    def test_get_orders_unauthorized(self):
        orders_response = requests.get(ORDER_URL)
        assert orders_response.status_code == 401
        assert orders_response.json() == EXPECTED_AUTH_ERROR_BODY
