from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
import email_validator

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')

class RegistrationForm(FlaskForm):
	username = StringField('Логин', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	password2 = PasswordField('Повтор пароля', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Зарегистрироваться')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Данное имя занято. Пожалуйста, выберите другое имя.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Пожалуйста, выберите другой email')

class PostForm(FlaskForm):
	post_title = TextAreaField('Введите название', validators=[
		DataRequired(), Length(min=1, max=64)])
	post = TextAreaField('Введите текст', validators=[
        DataRequired(), Length(min=1, max=1000)])
	submit = SubmitField('Опубликовать')