from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import  Length, Email, DataRequired
 
 
class Login(FlaskForm):
	email = StringField('Email', validators= [DataRequired(), Email(), Length(1,65)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Login')
