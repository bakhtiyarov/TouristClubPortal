from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config
import os

app = Flask('Hiking Club', template_folder='./app/templates')
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
from app import views, models
