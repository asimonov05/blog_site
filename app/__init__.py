from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__, static_folder="static_dir")
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Войдите в аккаунт, чтобы получить доступ к этой странице'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from app import routes, models, errors