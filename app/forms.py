from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SelectField, StringField, PasswordField, SubmitField, FileField, BooleanField, FloatField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange

from .models.user import User


class RegistrationForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired(), Length(min=2, max=100)])
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Данный логин занят. Пожалуйста выберите другой!')
        
class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')

class UpdateProfileForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired(), Length(min=2, max=100)])
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    current_password = PasswordField('Текущий пароль')
    new_password = PasswordField('Новый пароль')
    confirm_new_password = PasswordField('Подтвердите новый пароль', validators=[EqualTo('new_password')])
    role = SelectField('Роль', choices=[('user', 'Пользователь'), ('admin', 'Администратор'), ('author', 'Автор'), ('seller', 'Продавец')], validators=[DataRequired()])

    def __init__(self, original_login, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.original_login = original_login

    def validate_login(self, login):
        if login.data != self.original_login:
            user = User.query.filter_by(login=login.data).first()
            if user:
                raise ValidationError('Данный логин занят. Пожалуйста выберите другой!')
                
class PromoCodeForm(FlaskForm):
    code = StringField('Промокод', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Применить')

class AddPromoCodeForm(FlaskForm):
    code = StringField('Код', validators=[DataRequired(), Length(max=50)])
    discount = FloatField('Скидка (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    expiration_date = DateField('Дата истечения', validators=[DataRequired()])
    submit = SubmitField('Добавить')

class UpdatePostForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Описание', validators=[DataRequired(), Length(min=2, max=500)])
    price = FloatField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    features = StringField('Характеристики', validators=[DataRequired(), Length(min=2, max=500)])
    gender = SelectField('Пол', choices=[('Мужской', 'Мужской'), ('Женский', 'Женский'), ('Унисекс', 'Унисекс')], validators=[DataRequired()])
    picture = FileField('Изображение', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')])
    submit = SubmitField('Сохранить изменения')

class UpdateBlogForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(), Length(min=2, max=100)])
    text = StringField('Текст', validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Сохранить изменения')

class BlogForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(), Length(min=2, max=100)])
    text = TextAreaField('Текст', validators=[DataRequired(), Length(min=2)])
    picture = FileField('Изображение')
    submit = SubmitField('Добавить')