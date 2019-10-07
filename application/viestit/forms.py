from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, HiddenField, validators, SubmitField
from application.suomennokset import pituus_validaatiovirheviesti

class ViestiPohjaLomake(FlaskForm):
    otsikko = StringField("otsikko",[validators.Length(min=4, max=100, message=pituus_validaatiovirheviesti)])
    teksti = TextAreaField("teksti",[validators.Length(min=4, max=1000, message=pituus_validaatiovirheviesti)])

    class Meta:
        csrf = False

class ViestiLomake(ViestiPohjaLomake):
    aiheet = SelectMultipleField("aihe", coerce=int, choices=[])
    vastattava_viesti = HiddenField() 
    nappi = SubmitField("Lisää viesti")

class ViestinMuokkausLomake(ViestiPohjaLomake):
    nappi = SubmitField("Muokkaa viestiä")

class ViestinHakuLomake(FlaskForm):
    aihe = StringField("Aihe")
    nimi = StringField("Kirjoittaja")
    ryhma = StringField("Ryhmältä")
    nappi = SubmitField("Hae")

    class Meta:
        csrf = False
