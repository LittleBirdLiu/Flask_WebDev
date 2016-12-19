from flask import  Flask,make_response,redirect, render_template, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import EqualTo, DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from flask_mail import Mail, Message
from threading import  Thread

import os

#os.path.abspath ==> 返回path 规范化的绝对路径
#os.path.dirname(__file__) ==> 返回path的目录
#__file__==> 这个文件.py 所在的路径，一般是相对路径
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__)
theSqliteURL = 'sqlite:///' + os.path.join(basedir, 'test.db')
# 重点: Mac 系统一定要给所在文件夹开放读写权限
theSqliteRepo = os.path.join(basedir, 'db_repository')

print(theSqliteURL)

# app configrture
app.config['SQLALCHEMY_DATABASE_URI'] = theSqliteURL
app.config['SQLALCHEMY_MIGRATE_REPO'] = theSqliteRepo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'hard code'
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SUBJECT_PREFIX'] = 'HELLO '
app.config['MAIL_SENDER'] = 'Allen <liu_heyu@126.com>'
# app.config['APP_ADMIN'] = os.environ.get('APP_ADMIN')
app.config['MAIL_USERNAME'] = 'liu_heyu@126.com'
app.config['MAIL_PASSWORD'] = '19910820'
app.config['APP_ADMIN'] = 'liu_heyu@126.com'

print(app.config)
manager = Manager(app)
b_app = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

# 配置mail

mail = Mail(app)


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
    password = PW_Form.password.data
    PasswordRes = PW_Form.validate_on_submit()
    message_PW  = None

    if PasswordRes  :
        user = User.query.filter_by(userName = PW_Form.name.data).first()
        print(User.query.all())
        print(user)
        if user is None:
            user = User(username= PW_Form.name.data)
            db.session.add(user)
            session['Known'] = False
            db.session.commit()
            print('APP ADMIN IS' + app.config['APP_ADMIN'])
            if app.config['APP_ADMIN']:
                send_mail(app.config['APP_ADMIN'],
                          'new user',
                          'mail/new_user',
                          user = user)

        else:
            session['Known'] = True
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
                           message = message_PW,
                           known = session.get('Known',False))

def async_sendmail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['MAIL_SENDER'], recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    # msg.html = render_template(template + '.html' , **kwargs)
    thr = Thread(target= async_sendmail, args=[app, msg])
    return thr

if __name__ == '__main__':
    app.run(debug= True)
    # manager.run()