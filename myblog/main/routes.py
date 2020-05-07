
from flask import render_template, request, Blueprint
from myblog.models import PostBlog
from myblog.utils import create_post_data_for_view

main = Blueprint('main', __name__)

@main.route('/', methods = ['GET'])
def wellcome():
    return render_template('index.html')

@main.route('/home', methods = ['GET'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = PostBlog.query.order_by(PostBlog.time.desc()).paginate(page=page, per_page=5)

    items = []
    for postdb in posts.items:
        post = create_post_data_for_view(postdb)
        items.append(post)
    posts.items = items
    return render_template("home.html", posts = posts)

@main.route('/about', methods = ['GET'])
def about():
    return render_template("about.html", title = 'About')
