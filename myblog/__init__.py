from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5555/?password=123456789"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '69a25a8cf3d67cf8faba217be2fe1a6d'  # protect against modifying cookie and cross site request forgery attack

db = SQLAlchemy()
db.init_app(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_tab'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '' # abc@gmail.com
app.config['MAIL_PASSWORD'] = '' # abc
mail = Mail(app)
from myblog import routes