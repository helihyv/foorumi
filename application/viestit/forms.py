from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField

class ViestiLomake(FlaskForm):
    otsikko = StringField("otsikko")
    teksti = TextAreaField("teksti")
    aiheet = SelectMultipleField("aihe", coerce=int) 

    class Meta:
        csrf = False
