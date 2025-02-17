import requests
from conftest import headers, get_user_data
from tests.test_create_user import REGISTER_URL




class TestCreateOrder:

    def test_authorized_create_order(self, headers, get_user_data):
        response = requests.request("POST", REGISTER_URL, headers=headers, data=get_user_data)
        assert response.status_code == 200



