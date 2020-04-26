from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

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

from myblog import routes