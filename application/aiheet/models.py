from application import db

viestiAihe = db.Table("ViestiAihe",
db.Column("viesti_id", db.Integer, db.ForeignKey("viesti.id"), primary_key=True),
db.Column("aihe_id", db.Integer, db.ForeignKey("aihe.id"), primary_key=True)  
)

class Aihe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aihe = db.Column(db.String(100), nullable=False)
    viestit = db.relationship("Viesti", secondary=viestiAihe, lazy="subquery",
    backref = db.backref("aiheet", lazy="subquery"))

    def __init__(self, aihe):
        self.aihe = aihe