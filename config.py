import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


class Config:
    base_path = Path(__file__).parent
    db_path = base_path / 'database' / 'database.db'

    DEBUG = bool(os.getenv('DEBUG'))

    TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
    DOMAIN = os.getenv('DOMAIN')

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{str(db_path)}'
