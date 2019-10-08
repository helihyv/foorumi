from application import db
from sqlalchemy.sql import text
from application.kayttajat.models import Kayttaja

luetut = db.Table("luetut",
db.Column("viesti_id", db.Integer, db.ForeignKey("viesti.id"), primary_key=True),
db.Column("lukija_id", db.Integer, db.ForeignKey("kayttaja.id"), primary_key=True)
)

class Viesti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kirjoitusaika = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    muokkausaika = db.Column(db.DateTime, nullable=True)
    otsikko = db.Column(db.String(100), nullable=False)
    teksti = db.Column(db.String(1000), nullable=False)
    kirjoittaja_id = db.Column(db.Integer, db.ForeignKey('kayttaja.id'), nullable=False)
    vastattu_id = db.Column(db.Integer, db.ForeignKey("viesti.id"), nullable=True)
    vastaukset = db.relationship("Viesti", backref=db.backref("vastattu", remote_side=[id], lazy=True))
    lukeneet = db.relationship(Kayttaja, secondary=luetut, lazy=True,
    backref=db.backref("luetut_viestit", lazy=True))

    def __init__(self, otsikko, teksti, aiheet, vastattu_id, kirjoittanut_kayttaja_id):
        self.otsikko = otsikko
        self.teksti = teksti
        self.aiheet = aiheet
        self.kirjoittaja_id = kirjoittanut_kayttaja_id
        if vastattu_id:
            self.vastattu_id = vastattu_id

    def onko_lukenut(self, kayttaja):
        if kayttaja in self.lukeneet:
            return True

        return False


    def ovatko_kaikki_lukeneet(self):
        kysely_kaikki_kayttajat = text("SELECT COUNT(kayttaja.id) FROM kayttaja")

        kaikki_kayttajat = db.engine.execute(kysely_kaikki_kayttajat)

        kysely_lukeneet = text("SELECT COUNT(kayttaja.id) FROM kayttaja"
                            " JOIN luetut ON kayttaja.id = luetut.lukija_id"
                            " WHERE luetut.viesti_id = :viesti_id")

        lukeneet = db.engine.execute(kysely_lukeneet, {"viesti_id" : self.id })

        if kaikki_kayttajat.first()[0] - lukeneet.first()[0] == 0:
            return True

        return False