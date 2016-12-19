from flask import render_template, redirect, request, url_for,flash
from flask_login import login_user
from . import auth
from .forms import Login
from ..modle import User
from ..modle import db



@auth.route('/login', methods=['GET', 'POST'])
def login():
	print('strat view load')
	form = Login()
	if form.validate_on_submit():
		print('Post method')
		# print(User.query.all())
		print(form.email.data)
		user = User.query.filter_by(email=form.email.data).first()
		print(user)
		print(user.ver_password(form.password.data))
		if user is not None and user.ver_password(form.password.data):
			login_user(user, remember=form.remeber_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))

	return render_template('auth/login.html', form = form)
