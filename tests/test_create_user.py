import json

import allure
import requests

from conftest import create_and_remove_user
from constants import USER, EMAIL, NAME, CONTENT_HEADER
from urls import REGISTER_URL
from utils import get_user_data


class TestCreateUser:

    @allure.title("Проверка создания уникального пользователя")
    def test_create_unique_user(self, create_and_remove_user):
        status_code = create_and_remove_user.status_code
        success = create_and_remove_user.json().get('success')
        assert status_code == 200 and success == True

    @allure.title("Проверка ошибки создания существующего пользователя")
    def test_create_not_unique_user(self, create_and_remove_user):
        user = create_and_remove_user.json().get(USER)
        existing_user_payload = json.dumps(get_user_data(user.get(EMAIL), user.get(NAME)))
        error_response = requests.post(REGISTER_URL, headers=CONTENT_HEADER, data=existing_user_payload)
        assert error_response.status_code == 403 and error_response.json() == {"success": False,
                                                                               "message": "User already exists"}

    @allure.title("Проверка ошибки создания пользователя без обязательного поля")
    def test_error_create_user_required_field(self):
        payload = json.dumps({
            "name": "Анна",
            "password": "123456789"
        })
        error_response = requests.post(REGISTER_URL, headers=CONTENT_HEADER, data=payload)
        assert (error_response.status_code == 403
                and error_response.json() == {"success": False,
                                              "message": "Email, password and name are required fields"})
