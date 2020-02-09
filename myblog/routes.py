from flask import render_template, request, redirect
from myblog import app
from myblog.models import *


@app.route('/', methods = ['GET'])
def helloWorld():
    return render_template('index.html')

@app.route('/signup', methods = ['GET'])
def signup():
    return render_template('loginsignup_page.html')

@app.route('/signup-tab', methods = ['GET', 'POST'])
def signup_tab():
    print("log log ")
    if(request.method == "GET"):
        return render_template('loginsignup_page.html', title = "signup")
    else:
        typePost = request.form.get("type")
        if(typePost == "change_content"):
            return render_template('signup_form.html')
        else:
            new_user = User(email = request.form.get("emailInput"), 
                            username = request.form.get("usernameInput"),
                            password = request.form.get("passwordInput"))

            db.session.add(new_user)
            db.session.commit()
            return render_template('signup_form.html')
        


@app.route('/login-tab', methods = ['GET', 'POST'])
def login_tab():
    if(request.method == "GET"):
        return render_template('loginsignup_page.html', title = "login")
    else:
        typePost = request.form.get("type")
        if(typePost == "change_content"):
            return render_template('login_form.html')
        else:
            return render_template('login_form.html')