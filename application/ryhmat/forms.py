from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, validators, SubmitField
from application.suomennokset import pituus_validaatiovirheviesti

class RyhmaLomake(FlaskForm):
    nimi = StringField("Ryhmän nimi", [validators.Length(min=4,max=100, message=pituus_validaatiovirheviesti)])
    nappi = SubmitField("Lisää ryhmä")

    class Meta:
        csrf = False

class LisaaJasenLomake(FlaskForm):
    jasenet = SelectMultipleField("uudet jäsenet", coerce=int)
    nappi = SubmitField("Lisää jäsen")

    class Meta:
        csrf = False
