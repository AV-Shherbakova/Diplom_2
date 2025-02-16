import json
import random
import string

import pytest


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


@pytest.fixture
def headers():
    return {
        'Content-Type': 'application/json'
    }


@pytest.fixture
def get_user_data():
    return json.dumps({
        "name": "Анна",
        "email": generate_random_string(9) + '@mail.ru',
        "password": "123456789"
    })
