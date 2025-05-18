from venv import logger
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..models.blog import Blog
from ..extentions import db
from ..functions import save_picture
from app.forms import UpdateBlogForm, BlogForm

blog = Blueprint('blog', __name__)

@blog.route('/blog')
def all():
    blogs = Blog.query.all()
    return render_template('blog/all.html', blogs=blogs)

@blog.route('/blog/create', methods=['POST', 'GET'])
def create():
    form = BlogForm()
    if current_user.role == 'author' or current_user.role == 'admin':
        if form.validate_on_submit():
            name = form.name.data
            text = form.text.data
            picture = form.picture.data

            if picture:
                picture_fn = save_picture(picture)
            else:
                picture_fn = None

            blog = Blog(name=name, text=text, picture=picture_fn, id_author=current_user.id)

            try:
                db.session.add(blog)
                db.session.commit()
                flash("Статья добавлена!", category='success')
                return redirect('/blog')

            except Exception as e:
                print(str(e))
                flash("Произошла ошибка при добавлении статьи.", category='error')
                return redirect('/blog/create')

        return render_template('blog/create.html', form=form)
    else:
        abort(403)

@blog.route('/blog/<int:blog_id>')
def full_blog(blog_id):
    full_blog = Blog.query.get_or_404(blog_id)
    return render_template('blog/full_blog.html',blog=full_blog)

@blog.route('/blog/<int:blog_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Проверка прав доступа
    if current_user.id != blog.id_author and current_user.role != 'admin':
        abort(403)

    form = UpdateBlogForm()
    if form.validate_on_submit():
        blog.name = form.name.data
        blog.text = form.text.data  # Исправлено поле content на text
        db.session.commit()
        flash('Блог успешно обновлён!', 'success')
        return redirect(url_for('blog.full_blog', blog_id=blog.id))

    elif request.method == 'GET':
        form.name.data = blog.name
        form.text.data = blog.text

    return render_template('blog/edit_blog.html', form=form, blog=blog)

@blog.route('/blog/<int:blog_id>/delete', methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Проверка прав доступа
    if current_user.id != blog.id_author and current_user.role != 'admin':
        abort(403)

    try:
        db.session.delete(blog)
        db.session.commit()
        flash('Блог успешно удалён!', 'success')
    except Exception as e:
        flash('Ошибка при удалении блога.', 'error')
        print(str(e))

    return redirect(url_for('blog.all'))