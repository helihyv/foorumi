from application import app, db
from flask import render_template
from flask_login import login_required
from application.kayttajat.models import Kayttaja
from application.ryhmat.models import Ryhma
from application.aiheet.models import Aihe


@app.route("/tilastot")
@login_required
def tilastot():
    eniten_kirjoittaneet_kayttajat = Kayttaja.eniten_kirjoittaneet()
    eniten_kirjoittaneet_ryhmat = Ryhma.eniten_kirjoittaneet()
    suosituimmat_aiheet = Aihe.suosituimmat()
    ryhmien_aihe_jakaumat = Aihe.ryhmien_aihe_jakaumat()
    return render_template("tilastot/tilastot.html", eniten_kirjoittaneet_kayttajat=eniten_kirjoittaneet_kayttajat, eniten_kirjoittaneet_ryhmat=eniten_kirjoittaneet_ryhmat, suosituimmat_aiheet=suosituimmat_aiheet, ryhmien_aihe_jakaumat=ryhmien_aihe_jakaumat)
