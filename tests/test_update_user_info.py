import requests

from conftest import create_and_remove_user
from constants import ACCESS_TOKEN, EXPECTED_AUTH_ERROR_BODY
from urls import GET_USER_INFO_URL, UPDATE_USER_INFO_URL
from utils import get_auth_header, generate_random_string

UPDATE_USER_DATA_NAME = {"name": "НовоеИмя"}
UPDATE_USER_DATA_EMAIL = {"email": generate_random_string(9) + '@mail.ru'}
UPDATE_USER_DATA_PASSWORD = {"password": "7878"}


class TestUpdateUserInfo:

    def test_update_authorized_user_info(self, create_and_remove_user):
        token = create_and_remove_user.json().get(ACCESS_TOKEN)
        assert token is not None
        headers_with_token = get_auth_header(token)
        get_user_info_response = requests.get(GET_USER_INFO_URL, headers=headers_with_token)
        assert get_user_info_response.status_code == 200
        patch_response1 = requests.patch(UPDATE_USER_INFO_URL, headers=headers_with_token, data=UPDATE_USER_DATA_NAME)
        assert patch_response1.status_code == 200
        patch_response2 = requests.patch(UPDATE_USER_INFO_URL, headers=headers_with_token, data=UPDATE_USER_DATA_EMAIL)
        assert patch_response2.status_code == 200
        patch_response3 = requests.patch(
            UPDATE_USER_INFO_URL,
            headers=headers_with_token,
            data=UPDATE_USER_DATA_PASSWORD
        )
        assert patch_response3.status_code == 200

    def test_update_unauthorized_user_info(self):
        error_response1 = requests.patch(UPDATE_USER_INFO_URL, json=UPDATE_USER_DATA_NAME)
        assert error_response1.status_code == 401
        assert error_response1.json() == EXPECTED_AUTH_ERROR_BODY
        error_response2 = requests.patch(UPDATE_USER_INFO_URL, json=UPDATE_USER_DATA_EMAIL)
        assert error_response2.status_code == 401
        assert error_response2.json() == EXPECTED_AUTH_ERROR_BODY
