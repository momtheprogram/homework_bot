from telegram import TelegramError
import telegram

import logging
import sys
import time
import os

import requests

from dotenv import load_dotenv


load_dotenv()

PRACTICUM_TOKEN = os.getenv('PR_TOKEN')
TELEGRAM_TOKEN = os.getenv('T_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}
START_MESSAGE = 'Запуск Бота'
REQUEST_STATUS_MESSAGE = 'Требуемый статус не был получен.'
NOT_JSON_MESSAGE = 'Вернулся не json'


def check_tokens() -> bool:
    """Проверяет наличие токенов."""
    tokens = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    return all(tokens)


def send_message(bot, message: str) -> None:
    """Отправить сообщение в телеграм."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug('Сообщение отправлено успешно')
    except TelegramError:
        logging.error('Сообщение не было отправлено.')
        raise()


def get_api_answer(timestamp: int) -> dict:
    """Сделать запрос к API."""
    url = ENDPOINT
    headers = HEADERS
    payload = {'from_date': timestamp}
    try:
        response = requests.get(url, headers=headers, params=payload)
        if response.status_code != 200:
            raise RuntimeError('REQUEST_STATUS_MESSAGE')
        if not response.json():
            logging.error(NOT_JSON_MESSAGE)
    except requests.exceptions.RequestException:
        raise RuntimeError()
    return response.json()


def check_response(response: dict) -> list:
    """Проверить ответ. Получить список домашек."""
    if not isinstance(response, dict):
        raise TypeError()
    if 'homeworks' not in response and 'current_date' not in response:
        raise KeyError()
    if not isinstance(response.get('homeworks'), list):
        raise TypeError()
    return response['homeworks']


def parse_status(homework: dict) -> str:
    """Получить информацию о статусе домашки."""
    try:
        status = homework['status']
        verdict = HOMEWORK_VERDICTS[status]
        name = homework['homework_name']
        return f'Изменился статус проверки работы "{name}". {verdict}'
    except KeyError:
        raise KeyError('Неожиданный статус работы')


def main():
    """Основная логика работы бота."""
    logging.info(START_MESSAGE)
    if not check_tokens():
        logging.critical("Нет токенов")
        sys.exit(1)

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    previos_homework = None

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            current_homework = homeworks[0]
            if current_homework is not None:
                if current_homework != previos_homework:
                    send_message(bot, parse_status(current_homework))
                    previos_homework = current_homework

        # except requests.exceptions.RequestException:
        #     logging.error(REQUEST_STATUS_MESSAGE)
        except TelegramError as error:
            message = f'Сбой отправки сообщения: {error}'
            logging.exception(message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    FORMAT = ('%(asctime)s, %(levelname)s, %(funcName)s, %(message)s')
    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        handlers=[
            logging.FileHandler(__file__ + '.log', encoding='UTF-8', mode='w'),
            logging.StreamHandler(sys.stdout)])
    main()
