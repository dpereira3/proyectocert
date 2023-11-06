from .default import *
import os

SECRET_KEY = os.getenv('SECRET_KEY_ENV')

APP_ENV = APP_ENV_PRODUCTION

SQLALCHEMY_DATABASE_URI = 'postgresql://'+ os.getenv('DB_USER') + ':' + os.getenv('DB_PASS') + '@' + os.getenv('DB_HOST') + ':5432/' + os.getenv('DB_NAME')