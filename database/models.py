from bootstrap import db


class TelegramUser(db.Model):
    __tablename__ = 'telegram_user'

    id = db.Column('id', db.VARCHAR(12), primary_key=True)
    name = db.Column('name', db.VARCHAR(12), nullable=False)

    subscriptions = db.relationship('Subscription', backref="user")


class Subscription(db.Model):
    __tablename__ = 'subscription'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column('chat_id', db.VARCHAR(12), nullable=False)
    device_id = db.Column('device_id', db.VARCHAR(50), nullable=False)
    address = db.Column('address', db.VARCHAR(255), nullable=False)

    telegram_user_id = db.Column(db.Integer, db.ForeignKey('telegram_user.id'), nullable=False)


db.drop_all()
db.create_all()
