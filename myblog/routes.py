import os
import secrets
from PIL import Image
from flask import render_template, request, url_for, flash, redirect
from myblog import app, db, bcrypt, mail
from myblog.models import *
from myblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required


def create_post_data_for_view(postdb):
    return  {
                'author': User.query.filter_by(id = postdb.user_id).first(),
                'title': postdb.title,
                'content': postdb.content,
                'date_posted': postdb.time,
                'id': postdb.id
            }

@app.route('/', methods = ['GET'])
def wellcome():
    return render_template('index.html')

@app.route('/home', methods = ['GET'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = PostBlog.query.order_by(PostBlog.time.desc()).paginate(page=page, per_page=5)

    # postsdb = PostBlog.query.all()
    items = []
    for postdb in posts.items:
        post = create_post_data_for_view(postdb)
        items.append(post)
    posts.items = items
    return render_template("home.html", posts = posts)

@app.route('/about', methods = ['GET'])
def about():
    return render_template("about.html", title = 'About')

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
            login_user(user, remember=False)
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
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login_form_wtform.html', form = form, title = "login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods =['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account',
                           image_file=image_file, form=form)

@app.route("/post/new", methods =['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = PostBlog(title = form.title.data, content = form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title = 'New Post', form = form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = PostBlog.query.get_or_404(post_id)
    post_view = create_post_data_for_view(post)
    return render_template('post.html', title=post_view['title'], post=post_view)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = PostBlog.query.get_or_404(post_id)
    post_view = create_post_data_for_view(PostBlog.query.get_or_404(post_id))
    if post_view['author'] != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = PostBlog.query.get_or_404(post_id)
    post_view = create_post_data_for_view(PostBlog.query.get_or_404(post_id))
    if post_view['author'] != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = PostBlog.query.filter_by(user_id=user.id)\
        .order_by(PostBlog.time.desc())\
        .paginate(page=page, per_page=5)
    
    items = []
    for postdb in posts.items:
        post = create_post_data_for_view(postdb)
        items.append(post)
    posts.items = items
    return render_template('user_posts.html', posts=posts, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='ftestflask@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
                {url_for('reset_token', token=token, _external=True)}
                If you did not make this request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)

@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login_tab'))
    return render_template('reset_request.html', form = form, title = "Reset Password")


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login_tab'))
    return render_template('reset_token.html', title='Reset Password', form=form)