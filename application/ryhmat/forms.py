from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, validators, SubmitField, HiddenField, ValidationError
from application.suomennokset import pituus_validaatiovirheviesti
from application.ryhmat.models import Ryhma

def validoiUniikkiNimi(form, field):

    ryhma = Ryhma.query.filter_by(nimi = field.data).first()

    if ryhma:
        raise ValidationError("Samanniminen ryhmä on jo olemassa")

class RyhmaPohjaLomake(FlaskForm):
    nimi = StringField("Ryhmän nimi", [
        validators.Length(min=4,max=100, message=pituus_validaatiovirheviesti),
        validoiUniikkiNimi
    ])

    class Meta:
        csrf = False

class LisaaRyhmaLomake(RyhmaPohjaLomake):

    palattava_sivu = HiddenField()
    nappi = SubmitField("Lisää ryhmä")

class MuutaRyhmanNimeaLomake(RyhmaPohjaLomake):

    nappi = SubmitField("Muokkaa nimeä")


class LisaaJasenLomake(FlaskForm):
    jasenet = SelectMultipleField("uudet jäsenet", coerce=int)
    nappi = SubmitField("Lisää jäsen")

    class Meta:
        csrf = False
