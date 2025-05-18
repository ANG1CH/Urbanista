from app.extentions import db
from datetime import datetime

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    post = db.relationship('Post', backref=db.backref('cart_items', lazy=True))

    def __init__(self, user_id, post_id, quantity=1):
        self.user_id = user_id
        self.post_id = post_id
        self.quantity = quantity

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'quantity': self.quantity,
            'post': {
                'id': self.post.id,
                'name': self.post.name,
                'price': self.post.price,
                'picture': self.post.picture
            }
        }

class PromoCode(db.Model):
    __tablename__ = 'promo_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount = db.Column(db.Float, nullable=False)  # Процент скидки
    expiration_date = db.Column(db.DateTime, nullable=False)

    def is_valid(self):
        return datetime.utcnow() <= self.expiration_date