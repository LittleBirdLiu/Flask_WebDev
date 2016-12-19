from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from config import config

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
moment = Moment()

def create_app(CONFIG_NAME):
	app = Flask(__name__)
	app.config.from_object(config[CONFIG_NAME])
	config[CONFIG_NAME].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	db.init_app(app)
	moment.init_app(app)
	#TODO add route and 404

	return app

