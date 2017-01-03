from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField , SelectField , TextAreaField
from flask_pagedown.fields import  PageDownField
from wtforms.validators import Required, Length, Email, ValidationError
from ..models import Role, User


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    name = StringField('What is your real name', validators=[Length(0, 64)])
    location = StringField('Where are you from', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class AdminEditProfileForm(Form):
    email = StringField('Email', validators=[Required(),
                                             Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[Required(),
                                                   Length(1, 64)])
    confirmed = BooleanField('Confirmed')
    # Selected Field 是一个向下多选框， coerec会将值转化成指定类型
    role = SelectField('Role', coerce=int)
    name = StringField('What is your real name', validators=[Length(0, 64)])
    location = StringField('Where are you from', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(AdminEditProfileForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email = field.data).first():
            raise ValidationError('Email have been registered')
    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username = field.data).first():
            raise ValidationError('User Name have been registered')

class PostForm(Form):
    body = PageDownField("What's your mind right now?", validators=[Required()])
    submit = SubmitField('Submit')
