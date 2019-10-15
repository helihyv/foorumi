from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, HiddenField
from application.suomennokset import pituus_validaatiovirheviesti

class AihePohjaLomake(FlaskForm):
    aihe = StringField("Aihe", [validators.Length(min=4, max=100, message=pituus_validaatiovirheviesti)])
    palattava_sivu = HiddenField()

    class Meta:
        csrf = False


class LisaaAiheLomake(AihePohjaLomake):
    nappi = SubmitField("Lisää aihe")

class MuokkaaAihettaLomake(AihePohjaLomake):
    nappi = SubmitField("Muokkaa aihetta")        


