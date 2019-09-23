from application import db
from sqlalchemy.sql import text

viesti_aihe = db.Table("viestiaihe",
                      db.Column("viesti_id", db.Integer, db.ForeignKey(
                          "viesti.id"), primary_key=True),
                      db.Column("aihe_id", db.Integer, db.ForeignKey(
                          "aihe.id"), primary_key=True)
                      )


class Aihe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aihe = db.Column(db.String(100), nullable=False)
    viestit = db.relationship("Viesti", secondary=viesti_aihe, lazy="subquery",
                              backref=db.backref("aiheet", lazy="subquery"))

    def __init__(self, aihe):
        self.aihe = aihe

    @staticmethod
    def suosituimmat():
        kysely = text("SELECT aihe.aihe, COUNT(viestiaihe.viesti_id) AS viestilkm FROM aihe"
                      " LEFT JOIN viestiaihe ON aihe.id = viestiaihe.aihe_id"
                      " GROUP BY aihe.id"
                      " ORDER BY viestilkm DESC"
                      " LIMIT 5")

        vastaus = db.engine.execute(kysely)

        suosituimmat = []

        for rivi in vastaus:
            suosituimmat.append({"aihe": rivi[0], "viestien_lkm": rivi[1]})

        return suosituimmat

    @staticmethod
    def ryhmien_aihe_jakaumat():
        kysely = text("SELECT ryhma.nimi, aihe.aihe, COUNT(viestiaihe.viesti_id) AS viestilkm FROM aihe"
                      " JOIN Viestiaihe ON aihe.id = Viestiaihe.aihe_id"
                      " JOIN viesti ON viestiaihe.viesti_id = viesti.id"
                      " JOIN kayttaja ON viesti.kirjoittaja_id = kayttaja.id"
                      " JOIN kayttajaryhma ON kayttaja.id = kayttajaryhma.kayttaja_id"
                      " JOIN ryhma ON kayttajaryhma.ryhma_id = ryhma.id"
                      " GROUP BY ryhma.id, aihe.aihe"
                      " ORDER BY ryhma.nimi ASC, viestilkm DESC"
                      )

        vastaus = db.engine.execute(kysely)

        aihe_jakauma = []

        for rivi in vastaus:
            if not rivi[0] == None:
                aihe_jakauma.append(
                    {"ryhma": rivi[0], "aihe": rivi[1], "viestien_lkm": rivi[2]})
            print(rivi)

        return aihe_jakauma
