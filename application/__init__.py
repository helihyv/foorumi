from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = OS.ENVIRON.GET("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from os import urandom

app.config["SECRET_KEY"] = urandom(32)

from flask_bootstrap import Bootstrap 

Bootstrap(app)

from application import views

from application.viestit import models
from application.viestit import views

from application.aiheet import models
from application.aiheet import views

from application.ryhmat import models
from application.ryhmat import views

from application.tilastot import views

from application.kayttajat import models
from application.kayttajat import views

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_lomake"
login_manager.login_message = "Toiminto edellyttää kirjautumista"

from application.kayttajat.models import Kayttaja

@login_manager.user_loader
def load_user(kayttaja_id):
    return Kayttaja.query.get(kayttaja_id)

try:
    db.create_all()
except:
    pass
