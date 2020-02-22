from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5432/?password=c_hFbTvTcJFwQw"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '69a25a8cf3d67cf8faba217be2fe1a6d'  # protect against modifying cookie and cross site request forgery attack

db = SQLAlchemy()
db.init_app(app)

from myblog import routes