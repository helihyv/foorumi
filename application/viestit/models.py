from application import db

class Viesti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kirjoitusaika = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    otsikko = db.Column(db.String(100), nullable=False)
    teksti = db.Column(db.String(1000), nullable=False)
    kirjoittaja_id = db.Column(db.Integer, db.ForeignKey('kayttaja.id'), nullable=False)
    vastattu_id = db.Column(db.Integer, db.ForeignKey("viesti.id"), nullable=True)
    vastaukset = db.relationship("Viesti", backref=db.backref("vastattu", remote_side=[id]))

    def __init__(self, otsikko, teksti, aiheet, vastattu_id, kirjoittanut_kayttaja_id):
        self.otsikko = otsikko
        self.teksti = teksti
        self.aiheet = aiheet
        self.kirjoittaja_id = kirjoittanut_kayttaja_id
        if vastattu_id:
            self.vastattu_id = vastattu_id

