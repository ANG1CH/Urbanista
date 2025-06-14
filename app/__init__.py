from flask import Flask
from markupsafe import escape

from .routes.main import main
from .routes.post import post
from .routes.user import user
from .routes.blog import blog
from .routes.admin import admin
from .routes.favorite import favorite as favorite_blueprint
from .routes.cart import cart
from .config import Config
from .extentions import db, migrate, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(main)
    app.register_blueprint(post)
    app.register_blueprint(user)
    app.register_blueprint(blog)
    app.register_blueprint(admin)
    app.register_blueprint(favorite_blueprint)
    app.register_blueprint(cart)

    # Создание папки для загрузки файлов, если её нет
    import os
    upload_folder = os.path.join(app.static_folder, 'upload')
    os.makedirs(upload_folder, exist_ok=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # LOGIN MANAGER
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Вы не можете получить доступ к данной странице. Сначала нужно выполнить вход'

    @app.template_filter('safe_text')
    def safe_text_filter(text):
        return escape(text)

    return app