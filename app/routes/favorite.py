from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from ..extentions import db
from ..models.favorite import Favorite
from ..models.post import Post

favorite = Blueprint('favorite', __name__)

@favorite.route('/favorites')
@login_required
def favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorite/favorites.html', favorites=favorites)

@favorite.route('/favorite/add/<int:product_id>')
@login_required
def add_to_favorites(product_id):
    product = Post.query.get_or_404(product_id)
    
    # Проверяем, не добавлен ли уже товар в избранное
    existing_favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if existing_favorite:
        flash('Этот товар уже в избранном', 'info')
    else:
        favorite = Favorite(user_id=current_user.id, product_id=product_id)
        db.session.add(favorite)
        db.session.commit()
        flash('Товар добавлен в избранное', 'success')
    
    return redirect(request.referrer or url_for('post.item_card', product_id=product_id))

@favorite.route('/favorite/remove/<int:product_id>')
@login_required
def remove_from_favorites(product_id):
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first_or_404()
    
    db.session.delete(favorite)
    db.session.commit()
    flash('Товар удален из избранного', 'success')
    
    return redirect(request.referrer or url_for('favorite.favorites')) 