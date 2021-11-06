import requests as requests

from config import Config

TELEGRAM_API_TOKEN = Config.TELEGRAM_API_TOKEN
DOMAIN = Config.DOMAIN


def send_message(chat_id, message):
    base_url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}'
    command_url = f'sendMessage?chat_id={chat_id}&text={message}'
    url = f'{base_url}/{command_url}'

    response = requests.get(url)
    return response.json()
