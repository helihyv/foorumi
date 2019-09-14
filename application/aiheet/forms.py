from flask_wtf import FlaskForm
from wtforms import StringField, validators
from application.suomennokset import pituus_validaatiovirheviesti

class AiheLomake(FlaskForm):
    aihe = StringField("Aihe", [validators.Length(min=4, max=100, message=pituus_validaatiovirheviesti)])

    class Meta:
        csrf = False

