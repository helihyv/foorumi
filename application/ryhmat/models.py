from application import db

class Ryhma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)

    def __init__(self, nimi):
        self.nimi = nimi
        