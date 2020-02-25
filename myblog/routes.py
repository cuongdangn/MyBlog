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
    form = RegistrationForm()
    if(request.method == "GET"):
        return render_template('signup_form_wtform.html', form = form, title = "signup")
    else:
        if form.validate_on_submit():
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        return render_template('signup_form_wtform.html', form = form, title = "signup")
        


@app.route('/login-tab', methods = ['GET', 'POST'])
def login_tab():
    form = LoginForm()
    if(request.method == "GET"):
  
        return render_template('login_form_wtform.html', form = form, title = "login")
     
    else:
        if form.validate_on_submit():
            if form.email.data == 'admin@blog.com' and form.password.data == 'Password':
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login_form_wtform.html', form = form, title = "login")