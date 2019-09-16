from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, SubmitField

class ViestiLomake(FlaskForm):
    otsikko = StringField("otsikko")
    teksti = TextAreaField("teksti")
    aiheet = SelectMultipleField("aihe", coerce=int) 
    nappi = SubmitField("Lisää viesti")

    class Meta:
        csrf = False
