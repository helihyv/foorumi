from application import db
from application import bcrypt
from sqlalchemy.sql import text


class Kayttaja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)
    tunnus = db.Column(db.String(40), unique=True, nullable=False)
    salasanaHash = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    kirjoitetut_viestit = db.relationship(
        'Viesti', backref=db.backref('kirjoittaja', lazy=False), lazy=True)

    def __init__(self, nimi, tunnus, salasana, admin):
        self.nimi = nimi
        self.tunnus = tunnus
        self.salasanaHash = bcrypt.generate_password_hash(
            salasana).decode("utf-8")
        self.admin = admin

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def eniten_kirjoittaneet():
        kysely = text("SELECT kayttaja.nimi, COUNT(viesti.kirjoittaja_id) AS viestilkm FROM kayttaja"
                      " LEFT JOIN viesti ON kayttaja.id = viesti.kirjoittaja_id"
                      " GROUP BY kayttaja.id"
                      " ORDER BY viestilkm DESC"
                      " LIMIT 5")

        vastaus = db.engine.execute(kysely)

        eniten_kirjoittaneet = []
        for rivi in vastaus:
            eniten_kirjoittaneet.append(
                {"nimi": rivi[0], "viestien_lkm": rivi[1]})

            print(rivi)

        return eniten_kirjoittaneet

    def vaihda_salasana(self, salasana):
        self.salasanaHash = bcrypt.generate_password_hash(salasana).decode("utf-8")
        db.session.commit()

    @staticmethod
    def onko_adminia():
        kysely = Kayttaja.query.filter(Kayttaja.admin == True)
        vastaus = db.session.query(kysely.exists()).first()
        return vastaus[0]
