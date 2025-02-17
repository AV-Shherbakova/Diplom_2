import json

import requests

from conftest import headers, get_user_data
from urls import REGISTER_URL


class TestCreateUser:

    def test_create_unique_user(self, headers, get_user_data):
        response = requests.request("POST", REGISTER_URL, headers=headers, data=get_user_data)
        assert response.status_code == 200

    def test_create_not_unique_user(self, headers, get_user_data):
        payload = get_user_data
        success_response = requests.request("POST", REGISTER_URL, headers=headers, data=payload)
        assert success_response.status_code == 200
        error_response = requests.request("POST", REGISTER_URL, headers=headers, data=payload)
        assert error_response.status_code == 403
        assert error_response.json() == {"success": False, "message": "User already exists"}

    def test_error_create_user_required_field(self, headers):
        payload = json.dumps({
            "name": "Анна",
            "password": "123456789"
        })
        error_response = requests.request("POST", REGISTER_URL, headers=headers, data=payload)
        assert error_response.status_code == 403
        assert error_response.json() == {"success": False, "message": "Email, password and name are required fields"}
