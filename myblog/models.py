from myblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique = True)
    username = db.Column(db.String, nullable=False, unique = True)
    password = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class PostBlog(db.Model):
    __tablename__ = "postblog"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String, nullable = False)
    time = db.Column(db.Date, nullable = False)

class Comment(db.Model):
    __tablename__  = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable  = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("postblog.id"), nullable=False)

# class Like(db.Model):
#     __tablename__ = "like"
#     content = db.Column(db.String, nullable  = False)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey("postblog.id"), nullable=False)
