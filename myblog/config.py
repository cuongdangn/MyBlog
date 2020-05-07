import os

class Config:
    SECRET_KEY =  os.environ.get('FLASK_MYBLOG_SECRETKEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER =  'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('FLASK_MYBLOG_EMAIL')
    MAIL_PASSWORD = os.environ.get('FLASK_MYBLOG_EMAIL_PASSWORD')