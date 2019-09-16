from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class KayttajaLomake(FlaskForm):
    nimi = StringField("Käyttäjän nimi")
    tunnus = StringField("Käyttäjätunnus")
    salasana = PasswordField("Salasana")
    nappi = SubmitField("Luo käyttäjätunnus")

    class Meta:
        csrf = False
