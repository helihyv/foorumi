from application import db

class Viesti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kirjoitusaika = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    otsikko = db.Column(db.String(100), nullable=False)
    teksti = db.Column(db.String(1000), nullable=False)
   # vastattuviesti = db.Column(db.Integer, db.ForeignKey("Viesti.id"))
   # vastaukset = db.relationship("Viesti", backref="Viesti", lazy="True")

    def __init__(self, otsikko, teksti, aiheet):
        self.otsikko = otsikko
        self.teksti = teksti
        self.aiheet = aiheet

