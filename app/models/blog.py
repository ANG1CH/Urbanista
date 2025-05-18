from datetime import datetime
from ..extentions import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    picture = db.Column(db.String(200))
    text = db.Column(db.Text)
    id_author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    date = db.Column(db.DateTime, default=datetime.utcnow)