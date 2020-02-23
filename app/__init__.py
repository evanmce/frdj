from config import Config
from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
# from flask_mail import Mail
from flask_migrate import Migrate
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# import logging
# from logging.handlers import SMTPHandler, RotatingFileHandler
# import os

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
# mail = Mail(app)
migrate = Migrate(app, db)
# moment = Moment(app)

from app import routes, models
