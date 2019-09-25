from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, ValidationError, HiddenField, SubmitField
from application.kayttajat.models import Kayttaja 
from application.suomennokset import pituus_validaatiovirheviesti

def validoiUniikkiTunnus(form, field): 

    kayttaja = Kayttaja.query.filter_by(tunnus = field.data).first()

    if kayttaja:
       raise ValidationError("Käyttäjätunnus on jo varattu.")
    

class KayttajaLomake(FlaskForm):
    nimi = StringField("Käyttäjän nimi", [validators.Length(min=4, max=100, message=pituus_validaatiovirheviesti)])
    tunnus = StringField("Käyttäjätunnus", [validators.Length(min=4, max=40, message=pituus_validaatiovirheviesti), validoiUniikkiTunnus])
    salasana = PasswordField("Salasana", [validators.Length(min=4, max=40, message=pituus_validaatiovirheviesti)])
    nappi = SubmitField("Luo käyttäjätunnus")
    class Meta:
        csrf = False

class KirjautumisLomake(FlaskForm):
    tunnus = StringField("Käyttäjätunnus",[validators.InputRequired()])
    salasana = PasswordField("Salasana",[validators.InputRequired()])
    seuraava_sivu = HiddenField()
    nappi = SubmitField("Kirjaudu")


    class Meta:
        csrf = False