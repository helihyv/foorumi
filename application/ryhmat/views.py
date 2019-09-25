from application import app, db
from flask import render_template, request, redirect, url_for
from application.ryhmat.models import Ryhma
from application.ryhmat.forms import LisaaRyhmaLomake, LisaaJasenLomake, MuutaRyhmanNimeaLomake
from application.kayttajat.models import Kayttaja
from flask_login import login_required

@app.route("/ryhmat", methods=["GET"])
@login_required
def ryhmat():
    return render_template("ryhmat/ryhmat.html", ryhmat = Ryhma.query.all(), form = LisaaRyhmaLomake())

@app.route("/ryhmat", methods=["POST"])
def ryhmat_luo():
    form = LisaaRyhmaLomake(request.form)

    if not form.validate():
        return render_template("ryhmat/ryhmat.html", form = form,  ryhmat = Ryhma.query.all())

    ryhma = Ryhma(form.nimi.data)
    db.session().add(ryhma)
    db.session().commit()

    return redirect(url_for("ryhma", ryhma_id=ryhma.id))

@app.route("/ryhmat/<ryhma_id>/", methods=["GET"])
def ryhma(ryhma_id):
    ryhma = Ryhma.query.get_or_404(ryhma_id)

    lisaa_jasen_lomake = LisaaJasenLomake()
    lisaa_jasen_lomake.jasenet.choices =[(kayttaja.id, kayttaja.nimi) for kayttaja in Kayttaja.query.all()]

    muokkaa_ryhmaa_lomake = MuutaRyhmanNimeaLomake()
    muokkaa_ryhmaa_lomake.nimi.data = ryhma.nimi

    return render_template("ryhmat/ryhma.html", ryhma = ryhma, lisaa_jasen_lomake = lisaa_jasen_lomake, muokkaa_ryhmaa_lomake = muokkaa_ryhmaa_lomake)

@app.route("/ryhmat/<ryhma_id>/jasenet", methods=["POST"])
def lisaa_jasenia(ryhma_id):
    
    ryhma = Ryhma.query.get_or_404(ryhma_id)
 
    form = LisaaJasenLomake(request.form)
    
    ryhma.jasenet = ryhma.jasenet + [Kayttaja.query.get(jasen_id) for jasen_id in form.jasenet.data ]
    
    db.session().commit()

    print(ryhma.jasenet)
    
    return redirect(url_for("ryhma", ryhma_id=ryhma_id))

@app.route("/ryhmat/<ryhma_id>/jasenet/<jasen_id>/poista", methods=["POST"])
def poista_jasenia(ryhma_id, jasen_id):

    ryhma = Ryhma.query.get_or_404(ryhma_id)
    jasen = Kayttaja.query.get_or_404(jasen_id)

    if jasen in ryhma.jasenet:
        ryhma.jasenet.remove(jasen)
        db.session.commit()

    return redirect(url_for("ryhma", ryhma_id = ryhma.id))

@app.route("/ryhmat<ryhma_id>/poista", methods=["POST"])
def ryhmat_poista(ryhma_id):
    ryhma = Ryhma.query.get_or_404(ryhma_id)

    db.session.delete(ryhma)
    db.session.commit()

    return redirect(url_for("ryhmat"))

@app.route("/ryhmat/<ryhma_id>/", methods=["POST"])
def ryhmat_muokkaa(ryhma_id):
    ryhma = Ryhma.query.get_or_404(ryhma_id)

    form = MuutaRyhmanNimeaLomake(request.form)

    if not form.validate():
        lisaa_jasen_lomake = LisaaJasenLomake()
        lisaa_jasen_lomake.jasenet.choices =[(kayttaja.id, kayttaja.nimi) for kayttaja in Kayttaja.query.all()]

        return render_template("ryhmat/ryhma.html", muokkaa_ryhman_nimea_lomake = form, lisaa_jasen_lomake = lisaa_jasen_lomake)

    ryhma.nimi = form.nimi.data

    db.session.commit()

    return redirect(url_for("ryhma", ryhma_id = ryhma.id))
