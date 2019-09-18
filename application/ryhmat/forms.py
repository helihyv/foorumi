from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, validators
from application.suomennokset import pituus_validaatiovirheviesti

class RyhmaLomake(FlaskForm):
    nimi = StringField("Ryhmän nimi", [validators.Length(min=4,max=100, message=pituus_validaatiovirheviesti)])

    class Meta:
        csrf = False

class LisaaJasenLomake(FlaskForm):
    jasenet = SelectMultipleField("uudet jäsenet", coerce=int)

    class Meta:
        csrf = False
