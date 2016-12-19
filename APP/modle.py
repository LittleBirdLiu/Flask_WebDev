from . import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	userName = db.Column(db.String(80), unique = True)
	def __init__(self, username):
		self.userName = username
	def __repr__(self):
		return '<User name> is %s' % self.userName


