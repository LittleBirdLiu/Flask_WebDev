import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'THIS HARD CODE'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	MAIL_SUBJECT_PREFIX = '[ALLEN]'
	MAIL_SENDER = 'liu_heyu@126.com'
	APP_ADMIN = os.environ.get('APP_ADMIN')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.126.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_SQLALCHEMY_DATABASE_URI') \
	                          or 'sqlite:///' + os.path.join(basedir, 'data-dev.db')

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_SQLALCHEMY_DATABASE_URI') \
	                          or 'sqlite:///' + os.path.join(basedir, 'data-test.db')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_SQLALCHEMY_DATABASE_URI') \
	                          or 'sqlite:///' + os.path.join(basedir, 'data-pro.db')

config = {
	'development' : DevelopmentConfig,
	'testing' : TestingConfig,
	'production' : ProductionConfig,
	'default' : DevelopmentConfig
}
