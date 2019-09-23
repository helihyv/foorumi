from application import app, db
from flask import render_template
from flask_login import login_required
from application.kayttajat.models import Kayttaja


@app.route("/tilastot")
@login_required
def tilastot():
    eniten_kirjoittaneet_kayttajat = Kayttaja.eniten_kirjoittaneet()
    return render_template("tilastot/tilastot.html", eniten_kirjoittaneet_kayttajat = eniten_kirjoittaneet_kayttajat)