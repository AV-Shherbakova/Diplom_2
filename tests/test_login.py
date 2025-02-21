import allure

from conftest import create_and_remove_user
from constants import PASSWORD, EMAIL, USER
from utils import login_user


class TestLogin:

    @allure.title("Проверка логина зарегистрированным пользователем")
    def test_existing_user_login(self, create_and_remove_user):
        user = create_and_remove_user.json().get(USER)
        login_body = {
            "email": user.get(EMAIL),
            "password": PASSWORD
        }
        assert login_user(login_body).status_code == 200

    @allure.title("Проверка ошибочного логина")
    def test_incorrect_user_data(self):
        payload = {
            "email": 4545,
            "password": 121212
        }
        login_response = login_user(payload)
        assert login_response.status_code == 401
        assert login_response.json() == {"success": False, "message": "email or password are incorrect"}
