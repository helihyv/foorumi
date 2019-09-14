from application import db

kayttajaRyhma = db.Table("KayttajaRyhma",
db.Column("kayttaja_id", db.Integer,db.ForeignKey("kayttaja.id"), primary_key=True),
db.Column("ryhma_id", db.Integer, db.ForeignKey("ryhma.id"), primary_key=True)
)
class Ryhma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)
    jasenet = db.relationship("Kayttaja", secondary=kayttajaRyhma, lazy="subquery",
    backref = db.backref("kayttajat", lazy="subquery"))

    def __init__(self, nimi):
        self.nimi = nimi
        