from application import app, db
from flask import render_template, request, redirect
from application.kayttajat.models import Kayttaja
from application.kayttajat.forms import KayttajaLomake

@app.route("/kayttajat/uusi")
def kayttajat_lomake():
    return render_template("kayttajat/uusi.html", form = KayttajaLomake())

@app.route("/kayttajat", methods=["POST"])
def kayttajat_luo():
    kayttaja = Kayttaja(request.form.get("nimi"), request.form.get("tunnus"), request.form.get("salasana"), False)
    db.session.add(kayttaja)
    db.session.commit()

    return redirect("/")