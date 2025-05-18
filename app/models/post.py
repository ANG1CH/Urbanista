from datetime import datetime
from ..extentions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    section = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    features = db.Column(db.String(1000))
    price = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    id_seller = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    category = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)