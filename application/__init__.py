from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"

app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

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

db.create_all()