from typing import Any

import requests as requests
from sqlalchemy.exc import NoResultFound

from bootstrap import db
from config import Config
from database.models import TelegramUser, Subscription

help_message = """
ТУТ ДОЛЖНО БЫТЬ ОПИСАНИЕ БОТА

Команды:
/help - Помощь
/add Добавить новый принтер (например - /add 12345 ул. Пушкина д. 63)
"""

add_subscription_bad_input_message = """
Некорректный формат запроса.
"""

add_subscription_success_message = """
Ваш запрос обработан.
"""

add_subscription_error_message = """
Что-то пошло не так. Не удалось обработать Ваш запрос.
"""


class Bot:
    TELEGRAM_API_TOKEN = Config.TELEGRAM_API_TOKEN
    DOMAIN = Config.DOMAIN

    def __init__(self):
        self._accepted_chat_id = None
        self._accepted_user_id = None
        self._accepted_user_name = None

    @staticmethod
    def send_message(chat_id: str, user_id: str, message: str):
        message_prefix = ""
        if not chat_id == user_id:
            user = TelegramUser.query.filter_by(id=user_id)
            message_prefix = Bot.create_mention(user.id, user.name) + ',\n'

        base_url = f'https://api.telegram.org/bot{Bot.TELEGRAM_API_TOKEN}'
        command_url = f'sendMessage?chat_id={chat_id}&text={message_prefix + message}'
        url = f'{base_url}/{command_url}'

        response = requests.get(url)
        return response.json()

    def accept_message(self, message: Any):
        self._accepted_chat_id = message['chat']['id']
        self._accepted_user_id = message['from']['id']
        self._accepted_user_name = message['from']['first_name']

        self.__add_user_if_not_exist(self._accepted_user_id, self._accepted_user_name)

        command_text = message['text']
        self.trigger_event(command_text)

    @staticmethod
    def create_mention(user_id: str, user_name: str):
        mention = f"[{user_name}](tg://user?id={user_id})"
        return mention

    def trigger_event(self, command_text: str):
        command_data = ' '.join(command_text.split(' ')[1:])

        if command_text.startswith('/start'):
            self._on_start()

        elif command_text.startswith('/help'):
            self._on_help()

        elif command_text.startswith('/add'):
            self._on_add(command_data)

    def _on_start(self):
        self.__print_help(self._accepted_chat_id, self._accepted_user_id)

    def _on_help(self):
        self.__print_help(self._accepted_chat_id, self._accepted_user_id)

    def __print_help(self, chat_id: str, user_id: str):
        self.send_message(chat_id, user_id, help_message)

    def _on_add(self, data: str):
        words = data.split(' ')
        device_id = words[0]
        address = ' '.join(words[1:])

        if not (device_id and address):
            self.send_message(self._accepted_chat_id, self._accepted_user_id, add_subscription_bad_input_message)
            return None

        self.__add_subscription(self._accepted_chat_id, self._accepted_user_id, device_id, address)

    def __add_subscription(self, chat_id: str, user_id: str, device_id: str, address: str):
        try:
            subscription = Subscription(chat_id=chat_id, device_id=device_id, address=address)
            user = TelegramUser.query.filter_by(id=user_id).one()
            user.subscriptions.append(subscription)
            db.session.commit()
            self.send_message(chat_id, user_id, add_subscription_success_message)
        except Exception:
            self.send_message(chat_id, user_id, add_subscription_error_message)

        print(Subscription.query.all())

    def __add_user_if_not_exist(self, id_, name):
        try:
            TelegramUser.query.filter_by(id=id_).one()
        except NoResultFound:
            user = TelegramUser(id=id_, name=name)
            db.session.add(user)
            db.session.commit()
