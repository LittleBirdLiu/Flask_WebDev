from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import EqualTo, DataRequired



class PasswordForm(FlaskForm):
    name = StringField('What is your name', validators= [DataRequired()])
    password = PasswordField('Please input your password',validators= [DataRequired()])
    inputAgain = PasswordField('Input again', validators=[DataRequired(),EqualTo('password', message='Input not ok')])
    submit  = SubmitField('Submit')
