from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

class KayttajaLomake(FlaskForm):
    nimi = StringField("Käyttäjän nimi")
    tunnus = StringField("Käyttäjätunnus")
    salasana = PasswordField("Salasana")

    class Meta:
        csrf = False
