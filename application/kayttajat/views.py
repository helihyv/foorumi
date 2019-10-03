from application import app, db, bcrypt
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from application.kayttajat.models import Kayttaja
from application.kayttajat.forms import KayttajaLomake, KirjautumisLomake, SalasananVaihtoLomake

@app.route("/kayttajat/uusi")
def kayttajat_lomake():
     # Jos ylläpitäjää ei vielä ole näytetään ylläpitäjän tunnuksen luomisen ohjeteksti
    admin = not Kayttaja.onko_adminia()


    return render_template("kayttajat/uusi.html", form=KayttajaLomake(), admin=admin)

@app.route("/kayttajat", methods=["POST"])
def kayttajat_luo():

    form = KayttajaLomake(request.form)
    
    if not form.validate():
        return render_template("kayttajat/uusi.html", form = form)

     # Jos ylläpitäjää ei vielä ole, luodaan ylläpitäjän tunnus - muuten tavallinen tunnus
    admin = not Kayttaja.onko_adminia()

    kayttaja = Kayttaja(form.nimi.data, form.tunnus.data,
                        form.salasana.data, admin)

    db.session.add(kayttaja)
    db.session.commit()

    login_user(kayttaja)

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

    if not form.validate():
        return render_template("kayttajat/kirjautumislomake.html", form=form)

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

@app.route("/kayttajat/salasananvaihto")
@login_required
def kayttajat_salasananvaihto():

    form = SalasananVaihtoLomake()
    return render_template("kayttajat/salasananvaihto.html", form = form)

@app.route("/kayttajat/salasananvaihto", methods=["POST"])
@login_required
def kayttajat_vaihda_salasana():
    form = SalasananVaihtoLomake(request.form)

    if not form.validate():
        return render_template("kayttajat/salasananvaihto.html", form = form)

    current_user.vaihda_salasana(form.uusi_salasana.data)

    return render_template("/kayttajat/salasananvaihto.html", onnistui=True, form = SalasananVaihtoLomake())


