from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from application.suomennokset import pituus_validaatiovirheviesti

class AiheLomake(FlaskForm):
    aihe = StringField("Aihe", [validators.Length(min=4, max=100, message=pituus_validaatiovirheviesti)])
    nappi = SubmitField("Lisää aihe")

    class Meta:
        csrf = False


