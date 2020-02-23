from flask import render_template, request, url_for, flash, redirect
from myblog import app
from myblog.models import *
from myblog.forms import RegistrationForm, LoginForm

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route('/', methods = ['GET'])
def wellcome():
    return render_template('index.html')

@app.route('/home', methods = ['GET'])
def home():
    return render_template("home.html", posts = posts)

# @app.route('/signup', methods = ['GET'])
# def signup():
#     return render_template('loginsignup_page.html')

@app.route('/signup-tab', methods = ['GET', 'POST'])
def signup_tab():
    if(request.method == "GET"):
        return render_template('loginsignup_page.html', title = "signup")
    else:
        typePost = request.form.get("type")
        form = RegistrationForm()
        if(typePost == "change_content"):
            return render_template('signup_form_wtform.html', form = form)
        else:
            # new_user = User(email = request.form.get("emailInput"), 
            #                 username = request.form.get("usernameInput"),
            #                 password = request.form.get("passwordInput"))

            # db.session.add(new_user)
            # db.session.commit()
            if form.validate_on_submit():
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('home'))
            return render_template('signup_form.html')
        


@app.route('/login-tab', methods = ['GET', 'POST'])
def login_tab():
    if(request.method == "GET"):
        return render_template('loginsignup_page.html', title = "login")
    else:
        typePost = request.form.get("type")
        if(typePost == "change_content"):
            form = LoginForm()
            return render_template('login_form_wtform.html', form = form)
        else:
            return render_template('login_form.html')