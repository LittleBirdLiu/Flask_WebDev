from flask import  Flask,make_response,redirect, render_template, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import EqualTo, DataRequired
from flask_sqlalchemy import SQLAlchemy,Model
from flask_script import Manager
import os

#os.path.abspath ==> 返回path 规范化的绝对路径
#os.path.dirname(__file__) ==> 返回path的目录
#__file__==> 这个文件.py 所在的路径，一般是相对路径
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__)
theSqliteURL = 'sqlite:///' + os.path.join(basedir, 'test.db')
print(theSqliteURL)
app.config['SQLALCHEMY_DATABASE_URL'] = theSqliteURL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard code'
manager = Manager(app)
b_app = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	userName = db.Column(db.String(80), unique = True)
	def __init__(self, username):
		self.userName = username
	def __repr__(self):
		return '<User name> is %s' % self.userName


@app.route('/')
def index():
    response = make_response('<h1>the page carry a cookie</h1>')
    response.set_cookie('answer','42')
    return  render_template('index.html', var = 'hello', current_time = datetime.utcnow())

@app.route('/user/<name_PY>')
def UserPage(name_PY):
    print('the date time is %s' % datetime.utcnow())
    return render_template('User.html', name = name_PY, current_time = datetime.utcnow())

class PasswordForm(FlaskForm):
    name = StringField('What is your name', validators= [DataRequired()])
    password = PasswordField('Please input your password',validators= [DataRequired()])
    inputAgain = PasswordField('Input again', validators=[DataRequired(),EqualTo('password', message='Input not ok')])
    submit  = SubmitField('Submit')

@app.route('/Submit', methods = ['GET','POST'])
def sumbitForm():
    PW_Form = PasswordForm()
    name_submit = None
    submitResult = PW_Form.validate_on_submit()
    password = PW_Form.password.data
    print(password)
    PasswordRes = PW_Form.validate_on_submit()
    message_PW  = None
    print(PasswordRes)
    print(submitResult)
    if PasswordRes and submitResult :
        session['name'] = PW_Form.name.data
        print(name_submit)
        PW_Form.name.data = ''
        message_PW = 'Set password OK'
        return redirect(url_for('sumbitForm'))
    if not PasswordRes and password is not None:
        flash('the password is not match , please check')
    return render_template('Form.html' ,
                           form1 = PW_Form,
                           name = session.get('name'),
                           message = message_PW)

if __name__ == '__main__':
    app.run(debug= True)


