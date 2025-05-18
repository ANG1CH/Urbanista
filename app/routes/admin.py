from flask import Blueprint, render_template
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from flask import flash, redirect, url_for, request

from ..models.blog import Blog
from ..models.user import User
from ..models.post import Post
from ..forms import AddPromoCodeForm, UpdateProfileForm, UpdatePostForm, UpdateBlogForm
from ..models.cart import PromoCode
from ..extentions import db, bcrypt


admin = Blueprint('admin', __name__)

@admin.route('/admin/blogs', methods=['POST', 'GET'])
def admin_blogs():
    blogs = Blog.query.all()
    return render_template('admin/blog_db.html', blogs=blogs)

@admin.route('/admin/users', methods=['POST', 'GET'])
def admin_users():
    users = User.query.all()
    return render_template('admin/user_db.html', users=users)

@admin.route('/admin/posts', methods=['POST', 'GET'])
def admin_posts():
    posts = Post.query.all()
    return render_template('admin/post_db.html', posts=posts)

@admin.route('/admin/add_promo', methods=['GET', 'POST'])
@login_required
def add_promo():
    if current_user.role != 'admin':
        abort(403)

    form = AddPromoCodeForm()
    if form.validate_on_submit():
        promo = PromoCode(
            code=form.code.data,
            discount=form.discount.data,
            expiration_date=form.expiration_date.data
        )
        db.session.add(promo)
        db.session.commit()
        flash('Промокод успешно добавлен!', 'success')
        return redirect(url_for('admin.add_promo'))

    return render_template('admin/add_promo.html', form=form)

@admin.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(user_id)
    form = UpdateProfileForm(original_login=user.login)

    print(f"POST data: {request.form}")
    if form.validate_on_submit():
        if form.name.data != user.name:
            user.name = form.name.data
        if form.login.data != user.login:
            user.login = form.login.data
        if form.new_password.data:
            if not form.confirm_new_password.data:
                flash('Пожалуйста, подтвердите новый пароль.', 'danger')
                return render_template('admin/edit_user.html', form=form, user=user)
            user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        if form.role.data != user.role:
            user.role = form.role.data
        db.session.commit()
        flash('Данные пользователя обновлены!', 'success')
        return redirect(url_for('admin.admin_users'))

    elif request.method == 'GET':
        form.name.data = user.name
        form.login.data = user.login
        form.role.data = user.role

    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь успешно удалён!', 'success')
    return redirect(url_for('admin.admin_users'))