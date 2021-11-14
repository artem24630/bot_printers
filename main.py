from api.endpoints import NotifyError, TelegramWebhook
from bootstrap import app, api

api.add_resource(NotifyError, '/api/v1/notifyError')
api.add_resource(TelegramWebhook, '/api/v1/telegramWebhook')

if __name__ == '__main__':
    app.run(debug=True, port=80)
