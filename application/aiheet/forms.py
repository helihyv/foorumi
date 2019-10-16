from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, HiddenField, ValidationError
from application.suomennokset import pituus_validaatiovirheviesti
from application.aiheet.models import Aihe
def validoiUniikkiAihe(form, field):
    aihe = Aihe.query.filter_by(aihe = field.data).first()
    if aihe:
        raise ValidationError("Aihe on jo olemassa")

class AihePohjaLomake(FlaskForm):
    aihe = StringField("Aihe", [
        validators.Length(min=4, max=100, message=pituus_validaatiovirheviesti), 
        validoiUniikkiAihe
    ])
    palattava_sivu = HiddenField()

    class Meta:
        csrf = False


class LisaaAiheLomake(AihePohjaLomake):
    nappi = SubmitField("Lisää aihe")

class MuokkaaAihettaLomake(AihePohjaLomake):
    nappi = SubmitField("Muokkaa aihetta")        


