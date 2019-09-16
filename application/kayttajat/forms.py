from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField

class KayttajaLomake(FlaskForm):
    nimi = StringField("Käyttäjän nimi")
    tunnus = StringField("Käyttäjätunnus")
    salasana = PasswordField("Salasana")

    class Meta:
        csrf = False

class KirjautumisLomake(FlaskForm):
    tunnus = StringField("Käyttäjätunnus")
    salasana = PasswordField("Salasana")
    seuraava_sivu = HiddenField()

    class Meta:
        csrf = False