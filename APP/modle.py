from . import db
from . import login_Manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_Manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(UserMixin ,db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	userName = db.Column(db.String(80), unique = True)
	email = db.Column(db.String(64), unique = True, index = True)
	password_hash = db.Column(db.String(128))


	def __init__(self, username, password, email):
		self.userName = username
		self.password = password
		self.email = email

	#这里主要是设定这个password的属性是一个只写属性，当想要读取的时候就会报ATTRIBUTE ERROR
	@property
	def password(self):
		raise AttributeError('password is nt the readable attribute')

	@password.setter
	def password(self, pasword):
		self.password_hash = generate_password_hash(pasword)

	def ver_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User name> is %s' % self.userName


