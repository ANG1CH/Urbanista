from flask import Blueprint, abort, redirect, render_template, request, flash
from flask_login import current_user
from sqlalchemy import or_

from ..extentions import db
from ..models.post import Post
from ..functions import save_picture
from ..forms import UpdateProfileForm, RegistrationForm


post = Blueprint('post', __name__)

@post.route('/post/create', methods=['POST', 'GET'])
def create():
    form = RegistrationForm()
    if current_user.role == 'seller' or current_user.role == 'admin':
        if request.method == 'POST':
            name = request.form.get('name')
            section = request.form.get('section')
            description = request.form.get('description')
            features = request.form.get('features')
            price = request.form.get('price')
            gender = request.form.get('gender')
            picture = request.files.get('picture')

            if picture:
                picture_fn = save_picture(picture)
            else:
                picture_fn = None
            
            post = Post(name=name, section=section, description=description, features=features, price=price, gender=gender, picture=picture_fn, id_seller=current_user.id)

            try:
                db.session.add(post)
                db.session.commit()
                flash("Товар добавлен!", category='success')
                return redirect('/product/all')

            except Exception as e:
                print(str(e))
                flash("Произошла ошибка при добавлении товара.", category='error')
                return redirect('/post/create')
        
        else:
            return render_template('/post/create.html', form=form)
        
    else:
        abort(403)

@post.route('/product/<int:product_id>')
def item_card(product_id):
    post = Post.query.get_or_404(product_id)
    return render_template('post/item_card.html', post=post)

@post.route('/product/all', methods=['POST', 'GET'])
def all():
    posts = Post.query.order_by(Post.name).all()
    return render_template('post/all.html', posts=posts)

@post.route('/post/<int:product_id>/update', methods=['POST', 'GET'])
def update(product_id):
    post = Post.query.get(product_id)
    form = UpdateProfileForm(original_login=current_user.login)
    if post.seller.id == current_user.id or current_user.role == 'admin':
        if request.method == 'POST':
            post.name = request.form.get('name')
            post.description = request.form.get('description')
            post.features = request.form.get('features')
            post.price = request.form.get('price')
            post.gender = request.form.get('gender')

            try:
                db.session.commit()
                flash("Карточка товара изменена!", category='success')
                return redirect('/product/all')

            except Exception as e:
                print(str(e))
                flash("Произошла ошибка при изменении карточки товара.", category='error')
                return redirect('/post/update')
        else:
            return render_template('/post/update.html', post=post, form=form)
    else:
        abort(403)

@post.route('/post/<int:product_id>/delete', methods=['POST', 'GET'])
def delete(product_id):
    post = Post.query.get(product_id)
    if post.seller.id == current_user.id or current_user.role == 'admin':
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Карточка товара удалена!", category='success')
            return redirect('/product/all')

        except Exception as e:
            print(str(e))
            flash("Произошла ошибка при удалении карточки товара.", category='error')
        
    else:
        abort(403)

@post.route('/product/woman', methods=['POST', 'GET'])
def woman_wear():
    woman_wear = Post.query.filter(or_(Post.gender=='Женский', Post.gender=='Унисекс')).all()
    return render_template('post/woman_wear.html', woman_wear=woman_wear)

@post.route('/product/man', methods=['POST', 'GET'])
def man_wear():
    man_wear = Post.query.filter(or_(Post.gender=='Мужской', Post.gender=='Унисекс')).all()
    return render_template('post/man_wear.html', man_wear=man_wear)

@post.route('/product/sweatshirt', methods=['POST', 'GET'])
def sweatshirt():
    sweatshirts = Post.query.filter_by(section='свитшот').all()
    return render_template('post/sweatshirt.html', sweatshirts=sweatshirts)

@post.route('/product/shoes', methods=['POST', 'GET'])
def shoes():
    shoes = Post.query.filter_by(section='обувь').all()
    return render_template('post/shoes.html', shoes=shoes)

@post.route('/product/bodysuit', methods=['POST', 'GET'])
def bodysuit():
    bodysuits = Post.query.filter_by(section='боди').all()
    return render_template('post/bodysuit.html', bodysuits=bodysuits)

@post.route('/product/jeans', methods=['POST', 'GET'])
def jeans():
    jeans = Post.query.filter_by(section='джинсы').all()
    return render_template('post/jeans.html', jeans=jeans)

@post.route('/product/caps', methods=['POST', 'GET'])
def caps():
    caps = Post.query.filter_by(section='кепка').all()
    return render_template('post/caps.html', caps=caps)

@post.route('/product/jackets', methods=['POST', 'GET'])
def jackets():
    jackets = Post.query.filter_by(section='куртка').all()
    return render_template('post/jackets.html', jackets=jackets)

@post.route('/product/long_sleeves', methods=['POST', 'GET'])
def long_sleeves():
    long_sleeves = Post.query.filter_by(section='лонгслив').all()
    return render_template('post/long_sleeves.html', long_sleeves=long_sleeves)

@post.route('/product/socks', methods=['POST', 'GET'])
def socks():
    socks = Post.query.filter_by(section='носки').all()
    return render_template('post/socks.html', socks=socks)

@post.route('/product/pants', methods=['POST', 'GET'])
def pants():
    pants = Post.query.filter_by(section='штаны').all()
    return render_template('post/pants.html', pants=pants)

@post.route('/product/shorts', methods=['POST', 'GET'])
def shorts():
    shorts = Post.query.filter_by(section='шорты').all()
    return render_template('post/shorts.html', shorts=shorts)

@post.route('/product/tops', methods=['POST', 'GET'])
def tops():
    tops = Post.query.filter_by(section='топ').all()
    return render_template('post/tops.html', tops=tops)

@post.route('/product/shirts', methods=['POST', 'GET'])
def shirts():
    shirts = Post.query.filter_by(section='рубашка').all()
    return render_template('post/shirts.html', shirts=shirts)