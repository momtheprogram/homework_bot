import sys
import os


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir_content = os.listdir(BASE_DIR)
HOMEWORK_FILENAME = 'homework.py'
# проверяем, что в корне репозитория лежит файл с домашкой
if (
        HOMEWORK_FILENAME not in root_dir_content
        or os.path.isdir(os.path.join(BASE_DIR, HOMEWORK_FILENAME))
):
    assert False, (
        f'В директории `{BASE_DIR}` не найден файл '
        f'с домашней работой `{HOMEWORK_FILENAME}`. '
    )

pytest_plugins = [
    'tests.fixtures.fixture_data'
]

os.environ['PRACTICUM_TOKEN'] = 'sometoken'
os.environ['TELEGRAM_TOKEN'] = '1234:abcdefg'
os.environ['TELEGRAM_CHAT_ID'] = '12345'

