from flask import render_template, request, url_for, flash, redirect
from myblog import app, db, bcrypt
from myblog.models import *
from myblog.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

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
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            
            return redirect(url_for('home'))
        return render_template('signup_form_wtform.html', form = form, title = "signup")
        


@app.route('/login-tab', methods = ['GET', 'POST'])
def login_tab():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if(request.method == "GET"):
        return render_template('login_form_wtform.html', form = form, title = "login")
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if(user and bcrypt.check_password_hash(user.password, form.password.data)):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                print(request)
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login_form_wtform.html', form = form, title = "login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')