from flask import render_template, redirect, request, url_for,flash, session
from flask_login import login_user,logout_user
from . import auth
from .forms import Login,registerForm
from ..modle import User
from ..modle import db
from ..email import send_mail


@auth.route('/login', methods=['GET', 'POST'])
def login():
	print('strat view load')
	form = Login()
	if form.validate_on_submit():
		print('Post method')
		# print(User.query.all())
		print(form.email.data)
		user = User.query.filter_by(email = form.email.data).first()
		print(user)
		password = form.password.data
		print('password is' + password)
		if user is not None and user.ver_password(password):
			login_user(user, remember=form.remember_me.data)
			return redirect(url_for('main.index'))

	return render_template('auth/login.html', form = form)

@auth.route('/logout', methods =['GET','POST'])
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/register', methods =['GET', 'POST'])
def register():
	form = registerForm()
	if form.validate_on_submit():
		user = User(username = form.UserName.data,
				email = form.email.data,
				password = form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_mail(user.email, 'Confirm your accout',
				  'auth/mail/confirm', user = user, token = token)
		flash('a confrimation email have been sent')
		print(User.query.all())
		return redirect(url_for('main.index'))
	return render_template('auth/Register.html', registerForm = form)