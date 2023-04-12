import logging
from collections import namedtuple
from contextlib import contextmanager
from http import HTTPStatus
from inspect import signature
from types import ModuleType


def check_function(scope: ModuleType, func_name: str, params_qty: int = 0):
    """If scope has a function with specific name and params with qty."""
    assert hasattr(scope, func_name), (
        f'Не найдена функция `{func_name}`. '
        'Не удаляйте и не переименовывайте её.'
    )

    func = getattr(scope, func_name)

    assert callable(func), (
        f'`{func_name}` должна быть функцией'
    )

    sig = signature(func)
    assert len(sig.parameters) == params_qty, (
        f'Функция `{func_name}` должна принимать '
        f'количество аргументов: {params_qty}'
    )


def check_docstring(scope: ModuleType, func_name: str):
    assert hasattr(scope, func_name), (
        f'Не найдена функция `{func_name}`. '
        'Не удаляйте и не переименовывайте её.'
    )
    assert getattr(scope, func_name).__doc__, (
        f'Убедитесь, что в функции `{func_name}` есть docstring.'
    )


def check_default_var_exists(scope: ModuleType, var_name: str) -> None:
    """
    If precode variable exists in scope with a proper type.

    :param scope: Module to look for a variable
    :param var_name: Variable you want to check
    :return: None. It's an assert
    """
    assert hasattr(scope, var_name), (
        f'Не найдена переменная `{var_name}`. '
        'Не удаляйте и не переименовывайте ее.'
    )
    var = getattr(scope, var_name)
    assert not callable(var), (
        f'`{var_name}` должна быть переменной, а не функцией.'
    )


@contextmanager
def check_logging(caplog, level, message):
    """
    Check if a log message of the specified level appears during code
    execution in the context manager.
    """
    with caplog.at_level(level):
        yield
        log_record = [
            record for record in caplog.records
            if record.levelname == logging.getLevelName(level)
        ]
        assert len(log_record) > 0, message


InvalidResponse = namedtuple('InvalidResponse', ('data', 'defected_key'))


class MockResponseGET:
    CALLED_LOG_MSG = 'Request is sent'

    def __init__(self, *args, random_timestamp=None,
                 http_status=HTTPStatus.OK, **kwargs):
        self.random_timestamp = random_timestamp
        self.status_code = http_status
        self.reason = ''
        self.text = ''
        logging.warn(MockResponseGET.CALLED_LOG_MSG)

    def json(self):
        data = {
            "homeworks": [],
            "current_date": self.random_timestamp
        }
        return data


class MockTelegramBot:
    def __init__(self, **kwargs):
        self._is_message_sent = False

    def send_message(self, chat_id=None, text=None, **kwargs):
        self.is_message_sent = True
        self.chat_id = chat_id
        self.text = text


class BreakInfiniteLoop(Exception):
    pass
