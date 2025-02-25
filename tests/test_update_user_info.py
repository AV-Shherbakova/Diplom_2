import allure
import requests

from conftest import create_and_remove_user
from constants import ACCESS_TOKEN, EXPECTED_AUTH_ERROR_BODY
from urls import GET_USER_INFO_URL, UPDATE_USER_INFO_URL
from utils import get_auth_header, generate_random_string

UPDATE_USER_DATA_NAME = {"name": "НовоеИмя"}
UPDATE_USER_DATA_EMAIL = {"email": generate_random_string(9) + '@mail.ru'}
UPDATE_USER_DATA_PASSWORD = {"password": "7878"}


class TestUpdateUserInfo:

    @allure.title("Проверка обновления данных пользователя авторизованным пользователем")
    def test_update_authorized_user_info(self, create_and_remove_user):
        token = create_and_remove_user.json().get(ACCESS_TOKEN)
        headers_with_token = get_auth_header(token)
        get_user_info_response = requests.get(GET_USER_INFO_URL, headers=headers_with_token)
        patch_response1 = requests.patch(UPDATE_USER_INFO_URL, headers=headers_with_token, data=UPDATE_USER_DATA_NAME)
        patch_response2 = requests.patch(UPDATE_USER_INFO_URL, headers=headers_with_token, data=UPDATE_USER_DATA_EMAIL)
        patch_response3 = requests.patch(
            UPDATE_USER_INFO_URL,
            headers=headers_with_token,
            data=UPDATE_USER_DATA_PASSWORD
        )
        assert patch_response3.status_code == 200 and patch_response3.json().get('success') is True
        assert get_user_info_response.status_code == 200 and get_user_info_response.json().get('success') is True
        assert patch_response1.status_code == 200 and patch_response1.json().get('success') is True
        assert patch_response2.status_code == 200 and patch_response2.json().get('success') is True

    @allure.title("Проверка обновления данных пользователя авторизованным пользователем")
    def test_update_unauthorized_user_info(self):
        error_response1 = requests.patch(UPDATE_USER_INFO_URL, json=UPDATE_USER_DATA_NAME)
        error_response2 = requests.patch(UPDATE_USER_INFO_URL, json=UPDATE_USER_DATA_EMAIL)
        assert error_response1.status_code == 401 and error_response1.json() == EXPECTED_AUTH_ERROR_BODY
        assert error_response2.status_code == 401 and error_response2.json() == EXPECTED_AUTH_ERROR_BODY
