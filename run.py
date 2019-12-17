import os

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, render_template, request, redirect
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5555/myblog?password=123456789"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)



@app.route('/', methods = ['GET', 'POST'])
def helloWorld():
    if request.method == "POST":
        if(request.form.get("formID") == "formSignUp"):
            user = User(email = request.form.get("email"), username = request.form.get("username"), password = request.form.get("password"))
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError as err:
                db.session.rollback()
                numemail = User.query.filter_by(email = request.form.get("email")).count()
                numusername = User.query.filter_by(username = request.form.get("username")).count()
                print(numemail)
                print(numusername)
                
       

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
