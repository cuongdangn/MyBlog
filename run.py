import os

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, render_template, request, redirect
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5555/?password=123456789"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)



@app.route('/', methods = ['GET'])
def helloWorld():
    return render_template('index.html')

@app.route('/signup', methods = ['GET'])
def signup():
    return render_template('loginsignupPage.html')

@app.route('/signup-tab', methods = ['GET', 'POST'])
def signup_tab():
    print("log log ")
    if(request.method == "GET"):
        return render_template('loginsignupPage.html', title = "signup")
    else:
        typePost = request.form.get("type")
        if(typePost == "change_content"):
            return render_template('signupForm.html')
        else:
            print(request.form.get("usernameInput"))
            return render_template('signupForm.html')
        


@app.route('/login-tab', methods = ['GET', 'POST'])
def login_tab():
    if(request.method == "GET"):
        return render_template('loginsignupPage.html', title = "login")
    else:
        typePost = request.form.get("type")
        if(typePost == "change_content"):
            return render_template('loginForm.html')
        else:
            return render_template('loginForm.html')
if __name__ == '__main__':
    app.run(debug=True)
