from datetime import datetime
from ..extentions import db

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    product = db.relationship('Post', backref=db.backref('favorited_by', lazy=True))

    def __repr__(self):
        return f'<Favorite {self.id}>' 