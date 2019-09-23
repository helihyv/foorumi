from application import app, db, bcrypt
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from application.kayttajat.models import Kayttaja
from application.kayttajat.forms import KayttajaLomake, KirjautumisLomake

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

    return redirect(url_for("login_lomake"))

@app.route("/login", methods = ["GET"])
def login_lomake():

     form = KirjautumisLomake()
     form.seuraava_sivu.data = request.args.get("next", default="/viestit")

     print (form.seuraava_sivu.data)
     return render_template("kayttajat/kirjautumislomake.html", form = form)


@app.route("/login", methods= ["POST"])
def login():
    form = KirjautumisLomake(request.form)

    kayttaja = Kayttaja.query.filter_by(tunnus = form.tunnus.data).first()

    if not kayttaja or not bcrypt.check_password_hash(kayttaja.salasanaHash, form.salasana.data):
         return render_template("kayttajat/kirjautumislomake.html", form = form, error = "Salasana tai käyttäjätunnus väärin")

    login_user(kayttaja)

    seuraava_sivu = form.seuraava_sivu.data
    if not seuraava_sivu:
          seuraava_sivu = "/viestit"

    return redirect(seuraava_sivu)

@app.route("/logout")
def logout():
     logout_user()
     return redirect(url_for("login"))
