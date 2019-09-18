from application import app, db
from flask import render_template, request, redirect
from application.kayttajat.models import Kayttaja
from application.kayttajat.forms import KayttajaLomake

@app.route("/kayttajat/uusi")
def kayttajat_lomake():
    return render_template("kayttajat/uusi.html", form = KayttajaLomake())

@app.route("/kayttajat", methods=["POST"])
def kayttajat_luo():

    form = KayttajaLomake(request.form)
    
    if not form.validate():
        return render_template("kayttajat/uusi.html", form = form)

    kayttaja = Kayttaja(form.nimi.data, form.tunnus.data, form.salasana.data, False)

    db.session.add(kayttaja)
    db.session.commit()

    return redirect("/")