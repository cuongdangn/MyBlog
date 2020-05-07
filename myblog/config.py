import os

class Config:
    SECRET_KEY = '69a25a8cf3d67cf8faba217be2fe1a6d'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost:5555/?password=123456789"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER =  'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''