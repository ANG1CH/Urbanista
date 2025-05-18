from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.cart import CartItem, PromoCode
from app.models.post import Post
from app.extentions import db
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from ..forms import PromoCodeForm
import math

cart = Blueprint('cart', __name__)

@cart.route('/cart')
@login_required
def view_cart():
    form = PromoCodeForm()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(float(item.post.price) * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    return render_template('cart/cart.html', 
                         cart_items=cart_items,
                         total_price=total_price,
                         total_items=total_items,
                         form=form,
                         discounted_price=None)

@cart.route('/cart/add/<int:post_id>', methods=['POST'])
@login_required
def add_to_cart(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            post_id=post_id
        ).first()

        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user_id=current_user.id, post_id=post_id)
            db.session.add(cart_item)

        db.session.commit()
        flash('Товар добавлен в корзину', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Произошла ошибка при добавлении товара в корзину', 'danger')
        print(f"Error adding to cart: {str(e)}")

    return redirect(request.referrer or url_for('post.all'))

@cart.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    try:
        validate_csrf(request.form.get('csrf_token'))
        cart_item = CartItem.query.get_or_404(item_id)
        if cart_item.user_id != current_user.id:
            flash('У вас нет прав для удаления этого товара', 'danger')
            return redirect(url_for('cart.view_cart'))
        
        db.session.delete(cart_item)
        db.session.commit()
        flash('Товар удален из корзины', 'success')
        return redirect(url_for('cart.view_cart'))
    except ValidationError:
        flash('Ошибка безопасности. Пожалуйста, попробуйте снова.', 'danger')
        return redirect(url_for('cart.view_cart'))
    except Exception as e:
        db.session.rollback()
        flash('Произошла ошибка при удалении товара из корзины', 'danger')
        print(f"Error removing from cart: {str(e)}")
        return redirect(url_for('cart.view_cart'))

@cart.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_quantity(item_id):
    try:
        validate_csrf(request.form.get('csrf_token'))
        cart_item = CartItem.query.get_or_404(item_id)
        if cart_item.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        action = request.form.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        
        db.session.commit()
        return redirect(url_for('cart.view_cart'))
    except ValidationError:
        flash('Ошибка безопасности. Пожалуйста, попробуйте снова.', 'danger')
        return redirect(url_for('cart.view_cart'))
    except Exception as e:
        db.session.rollback()
        flash('Произошла ошибка при обновлении количества товара', 'danger')
        print(f"Error updating quantity: {str(e)}")
        return redirect(url_for('cart.view_cart'))

@cart.route('/cart/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(float(item.post.price) * item.quantity for item in cart_items)

    # Возвращаем JSON с данными для виджета ЮKassa
    return jsonify({
        "confirmation_token": "Ваш_токен_подтверждения",  # Замените на реальный токен
        "total_price": total_price
    })

@cart.route('/apply_promo', methods=['POST'])
def apply_promo():
    form = PromoCodeForm()
    if form.validate_on_submit():
        promo = PromoCode.query.filter_by(code=form.code.data).first()
        if promo and promo.is_valid():
            discount = promo.discount
            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
            total_price = sum(float(item.post.price) * item.quantity for item in cart_items)
            discounted_price = math.floor(total_price * (1 - discount / 100) * 100) / 100
            flash(f'Промокод применён! Скидка: {discount}%. Итоговая сумма: ₽{discounted_price:.2f}', 'success')
            return render_template('cart/cart.html', 
                                   cart_items=cart_items,
                                   total_price=total_price,
                                   discounted_price=discounted_price,
                                   total_items=sum(item.quantity for item in cart_items),
                                   form=form)
        else:
            flash('Неверный или истёкший промокод.', 'danger')
    return redirect(url_for('cart.view_cart'))