import flask
from flask_restful import Resource

from api import telegram
from api.telegram import Bot
from database.models import Subscription


class NotifyError(Resource):
    def post(self):
        data = flask.request.get_json()
        server_message = data['message']
        device_id = data['tablet_id']

        subscriptions = Subscription.query.all()
        for subscription in subscriptions:
            if subscription.device_id == device_id:
                message = f"{server_message}\n\nID принтера: {device_id}\nАдрес: {subscription.address}"
                Bot.send_message(subscription.chat_id, subscription.user.id, message)


class TelegramWebhook(Resource):
    def post(self):
        data = flask.request.get_json()
        message = data['message']

        bot = telegram.Bot()
        bot.accept_message(message)
