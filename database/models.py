from bootstrap import db


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.VARCHAR(12), nullable=False)
    device_id = db.Column('device_id', db.VARCHAR(50), nullable=False)


db.create_all()
