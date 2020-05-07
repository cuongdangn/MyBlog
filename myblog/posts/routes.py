from flask import render_template, request, url_for, flash, redirect, Blueprint, abort
from myblog import db
from myblog.models import PostBlog
from myblog.posts.forms import PostForm
from flask_login import current_user, login_required
from myblog.utils import create_post_data_for_view

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods =['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = PostBlog(title = form.title.data, content = form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = 'New Post', form = form)

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = PostBlog.query.get_or_404(post_id)
    post_view = create_post_data_for_view(post)
    return render_template('post.html', title=post_view['title'], post=post_view)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = PostBlog.query.get_or_404(post_id)
    post_view = create_post_data_for_view(PostBlog.query.get_or_404(post_id))
    if post_view['author'] != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
