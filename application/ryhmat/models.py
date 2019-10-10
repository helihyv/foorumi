from application import db
from sqlalchemy import text

kayttajaRyhma = db.Table("kayttajaryhma",
                         db.Column("kayttaja_id", db.Integer, db.ForeignKey(
                             "kayttaja.id"), primary_key=True),
                         db.Column("ryhma_id", db.Integer, db.ForeignKey(
                             "ryhma.id"), primary_key=True)
                         )


class Ryhma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)
    jasenet = db.relationship("Kayttaja", secondary=kayttajaRyhma, lazy=True,
                              backref=db.backref("ryhmat", lazy=True))

    def __init__(self, nimi):
        self.nimi = nimi

    @staticmethod
    def eniten_kirjoittaneet():
        kysely = text("SELECT ryhma.nimi, COUNT(viesti.kirjoittaja_id) AS viestilkm FROM ryhma"
                      " LEFT JOIN kayttajaryhma ON ryhma.id = kayttajaryhma.ryhma_id"
                      " LEFT JOIN viesti ON kayttajaryhma.kayttaja_id = viesti.kirjoittaja_id"
                      " GROUP BY ryhma.id"
                      " ORDER BY viestilkm DESC"
                      " LIMIT 5")

        vastaus = db.engine.execute(kysely)

        eniten_kirjoittaneet = []

        for rivi in vastaus:
            eniten_kirjoittaneet.append(
                {"nimi": rivi[0], "viestien_lkm": rivi[1]})


        return eniten_kirjoittaneet
