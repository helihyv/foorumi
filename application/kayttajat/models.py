from application import db
from application import bcrypt

class Kayttaja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)
    tunnus = db.Column(db.String(40), unique=True, nullable=False)
    salasanaHash = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, nimi, tunnus, salasana, admin):
        self.nimi = nimi
        self.tunnus = tunnus
        self.salasanaHash = bcrypt.generate_password_hash(salasana).decode("utf-8")
        self.admin = admin
