from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import  Length, Email, DataRequired, Regexp, EqualTo
from wtforms import ValidationError
from ..modle import  User

 
class Login(FlaskForm):
	email = StringField('Email', validators= [DataRequired(), Email(), Length(1,65)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Login')


class registerForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(),
											 Email(),
											 Length(1,65)])
	UserName = StringField('Username', validators=[DataRequired(),
												   Length(1,65),
												   Regexp('^[A-Za-z0-9_.]*$',0,
														  'User name must be letter, number')])
	password = PasswordField('Password', validators=[DataRequired(),
													 EqualTo('password_ver', message='password must match')])
	password_ver = PasswordField('Input again', validators=[DataRequired()])
	submit = SubmitField('Submit')

	def validate_email(self, field):
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('EMAIL aleray register')


	def validate_username(self, field):
		if User.query.filter_by(userName = field.data).first():
			raise ValidationError('User name have been register')

