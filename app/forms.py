from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SelectMultipleField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from config import Config

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    year = IntegerField('Год', validators=[DataRequired(), NumberRange(min=0, max=2026)])
    publisher = StringField('Издательство', validators=[DataRequired(), Length(max=200)])
    author = StringField('Автор', validators=[DataRequired(), Length(max=200)])
    pages = IntegerField('Объём (страницы)', validators=[DataRequired(), NumberRange(min=1)])
    genres = SelectMultipleField('Жанры', coerce=int, validators=[DataRequired()])
    cover = FileField('Обложка', validators=[
        DataRequired(message='Обложка обязательна для загрузки'),  # Добавлено!
        FileAllowed(Config.ALLOWED_EXTENSIONS, 'Только изображения!')
    ])

class ReviewForm(FlaskForm):
    rating = SelectField('Оценка', choices=[
        (5, '5 – отлично'),
        (4, '4 – хорошо'),
        (3, '3 – удовлетворительно'),
        (2, '2 – неудовлетворительно'),
        (1, '1 – плохо'),
        (0, '0 – ужасно')
    ], coerce=int, validators=[DataRequired()])
    text = TextAreaField('Текст рецензии', validators=[DataRequired()])

class SearchForm(FlaskForm):
    title = StringField('Название', validators=[Optional()])
    genre = SelectMultipleField('Жанр', coerce=int, validators=[Optional()])
    year = SelectMultipleField('Год', coerce=int, validators=[Optional()])
    pages_from = IntegerField('Объём от', validators=[Optional(), NumberRange(min=1)])
    pages_to = IntegerField('Объём до', validators=[Optional(), NumberRange(min=1)])
    author = StringField('Автор', validators=[Optional()])