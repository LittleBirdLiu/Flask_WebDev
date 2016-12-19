from datetime import datetime
from flask import session, render_template, redirect,url_for, flash, current_app
from .. import db
from ..modle import User
from ..email import send_mail
from . import main
from .forms import PasswordForm

@main.route('/')
def index():
    return render_template('index.html',  current_time= datetime.utcnow())


@main.route('/user/<name>')
def UserPage(name):
    user = User.query.filter_by(userName = name).first()
    if user is None:
        return redirect(url_for('.submitForm'))
    else:
        return render_template('User.html', name = user, current_time= datetime.utcnow())


@main.route('/submit', methods = ['GET','POST'])
def submitForm():
    form = PasswordForm()
    submitName = None
    if form.validate_on_submit():
        user = User.query.filter_by(userName = form.name.data).first()
        print(User.query.all())
        print(user)
        if user is None:
            user = User(form.name.data)
            db.session.add(user)
            session['Known'] = False
            db.session.commit()
        else:
            session['Known'] = True

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.submitForm'))

    return render_template('Form.html',
                           form1=form,
                           name=session.get('name'),
                           message="Hello",
                           known=session.get('Known', False))



