import json

import requests

from conftest import create_and_remove_user
from constants import USER, EMAIL, NAME
from urls import REGISTER_URL
from utils import get_user_data, get_content_header


class TestCreateUser:

    def test_create_unique_user(self, create_and_remove_user):
        assert create_and_remove_user.status_code == 200

    def test_create_not_unique_user(self, create_and_remove_user):
        assert create_and_remove_user.status_code == 200
        user = create_and_remove_user.json().get(USER)
        existing_user_payload = json.dumps(get_user_data(user.get(EMAIL), user.get(NAME)))
        error_response = requests.post(REGISTER_URL, headers=get_content_header(), data=existing_user_payload)
        assert error_response.status_code == 403
        assert error_response.json() == {"success": False, "message": "User already exists"}

    def test_error_create_user_required_field(self):
        payload = json.dumps({
            "name": "Анна",
            "password": "123456789"
        })
        error_response = requests.post(REGISTER_URL, headers=get_content_header(), data=payload)
        assert error_response.status_code == 403
        assert error_response.json() == {"success": False, "message": "Email, password and name are required fields"}
