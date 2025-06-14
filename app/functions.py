import secrets
import os.path
from flask import current_app


def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    # Корректный путь для сохранения файла
    upload_folder = os.path.join(current_app.static_folder, 'upload')
    os.makedirs(upload_folder, exist_ok=True)
    picture_path = os.path.join(upload_folder, picture_fn)
    picture.save(picture_path)
    return picture_fn