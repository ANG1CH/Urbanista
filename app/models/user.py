from datetime import datetime
from flask_login import UserMixin

from ..extentions import db, login_manager
from ..models.post import Post
from ..models.blog import Blog


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(250), default='user')
    name = db.Column(db.String(250))
    login = db.Column(db.String(50))
    password = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship(Post, backref='seller')
    blogs = db.relationship(Blog, backref='author')