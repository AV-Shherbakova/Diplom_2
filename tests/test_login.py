import json

import requests

from conftest import headers, get_user_data
from tests.test_create_user import REGISTER_URL, LOGIN_URL


class TestLogin:

    def test_existing_user_login(self, headers, get_user_data):
        requests.request("POST", REGISTER_URL, headers=headers, data=get_user_data)
        user_object = json.loads(get_user_data)
        payload = json.dumps({
            "email": user_object.get("email"),
            "password": user_object.get("password")
        })
        login_response = requests.request("POST", LOGIN_URL, headers=headers, data=payload)
        assert login_response.status_code == 200

    def test_incorrect_user_data(self, headers):
        payload = json.dumps({
            "email": 4545,
            "password": 121212
        })
        login_response = requests.request("POST", LOGIN_URL, headers=headers, data=payload)
        assert login_response.status_code == 401
        assert login_response.json() == {"success": False, "message": "email or password are incorrect"}
