import random
import string
from datetime import datetime

import pytest


@pytest.fixture
def random_timestamp():
    left_ts = 1000198000
    right_ts = 1000198991
    return random.randint(left_ts, right_ts)


@pytest.fixture
def current_timestamp():
    return int(datetime.now().timestamp())


@pytest.fixture
def homework_module():
    import homework
    return homework


@pytest.fixture
def random_message():
    def random_string(string_length=15):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(string_length))
    return random_string()
