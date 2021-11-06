import flask
from flask_restful import Resource

from api import telegram
from bootstrap import db
from database.models import Client


class NotifyError(Resource):
    def post(self):
        data = flask.request.get_json()
        message = data['message']
        device_id = data['tablet_id']
        clients = Client.query.filter_by(device_id=device_id).all()

        for client in clients:
            telegram.send_message(client.user_id, message)


class AddClient(Resource):
    def post(self):
        data = flask.request.get_json()
        message = data['message']
        client_id = message['from']['id']
        chat_id = message['chat']['id']
        text = message['text']

        try:
            client = Client(user_id=client_id, device_id=text)
            db.session.add(client)
            db.session.commit()

            success_message = "Вы добавлены в базу данных."
            telegram.send_message(chat_id, success_message)
        except Exception:
            error_message = "Что-то пошло не так. Не удалось добавить Вас в базу данных."
            telegram.send_message(chat_id, error_message)
