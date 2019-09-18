from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, HiddenField, validators
from application.suomennokset import pituus_validaatiovirheviesti

class ViestiLomake(FlaskForm):
    otsikko = StringField("otsikko",[validators.Length(min=4, max=100, message=pituus_validaatiovirheviesti)])
    teksti = TextAreaField("teksti",[validators.Length(min=4, max=1000, message=pituus_validaatiovirheviesti)])
    aiheet = SelectMultipleField("aihe", coerce=int, choices=[])
    vastattava_viesti = HiddenField() 

    class Meta:
        csrf = False
