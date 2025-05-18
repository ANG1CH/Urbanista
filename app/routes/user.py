from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

from ..forms import LoginForm, RegistrationForm, UpdateProfileForm
from ..extentions import db, bcrypt
from ..models.user import User


user = Blueprint('user', __name__)

@user.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        login = form.login.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(name=name, login=login, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт был создан!', 'success')
        return redirect(url_for('user.login'))

    return render_template('user/register.html', form=form)

@user.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вы вошли в систему!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Вход не выполнен. Проверьте логин и пароль.', 'danger')

    return render_template('user/login.html', form=form)

@user.route('/user/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@user.route('/user/profile', methods=['POST', 'GET'])
def profile():
    profiles = User.query.all()
    return render_template('user/profile.html', profiles=profiles)

@user.route('/user/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm(original_login=current_user.login)
    if form.validate_on_submit():
        if form.current_password.data:
            if bcrypt.check_password_hash(current_user.password, form.current_password.data):
                if form.new_password.data:
                    current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            else:
                flash('Неверный текущий пароль', 'danger')
                return render_template('user/update_profile.html', form=form)
        
        current_user.name = form.name.data
        current_user.login = form.login.data
        
        try:
            db.session.commit()
            flash('Профиль успешно обновлен!', 'success')
            return redirect(url_for('user.profile'))
        except Exception as e:
            print(str(e))
            flash('Произошла ошибка при обновлении профиля', 'danger')
            return render_template('user/update_profile.html', form=form)
    
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.login.data = current_user.login
    
    return render_template('user/update_profile.html', form=form)