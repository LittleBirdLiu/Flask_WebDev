from flask import  Flask
from flask import make_response,redirect, render_template, url_for, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  Required, EqualTo, DataRequired

from flask_script import Manager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard code'
manager = Manager(app)
b_app = Bootstrap(app)
moment = Moment(app)


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
    name = StringField('What is your name', validators= [Required()])
    password = PasswordField('Please input your password',validators= [DataRequired()])
    inputAgain = PasswordField('Input again', validators=[Required(),EqualTo('password', message='Input not ok')])
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
    return render_template('Form.html' ,
                           form1 = PW_Form,
                           name = session.get('name'),
                           message = message_PW)

if __name__ == '__main__':
    app.run(debug= True)


