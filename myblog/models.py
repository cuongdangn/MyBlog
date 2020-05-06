from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from myblog import db, login_manager, app
from flask_login import UserMixin
import datetime
from flask_mail import Message


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

    def get_reset_token(self, expires_sec = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class PostBlog(db.Model):
    __tablename__ = "postblog"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String, nullable = False)
    time = db.Column(db.Date, nullable = False, default = datetime.datetime.utcnow)


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
