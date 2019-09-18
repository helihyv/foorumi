from application import app, db
from flask import render_template, request, redirect, url_for
from application.ryhmat.models import Ryhma
from application.ryhmat.forms import RyhmaLomake, LisaaJasenLomake
from application.kayttajat.models import Kayttaja
from flask_login import login_required

@app.route("/ryhmat", methods=["GET"])
@login_required
def ryhmat():
    return render_template("ryhmat/ryhmat.html", ryhmat = Ryhma.query.all(), form = RyhmaLomake())

@app.route("/ryhmat", methods=["POST"])
def ryhmat_luo():
    form = RyhmaLomake(request.form)

    if not form.validate():
        return render_template("ryhmat/ryhmat.html", form = form,  ryhmat = Ryhma.query.all())

    ryhma = Ryhma(form.nimi.data)
    db.session().add(ryhma)
    db.session().commit()

    return redirect(url_for("ryhma", ryhma_id=ryhma.id))

@app.route("/ryhmat/<ryhma_id>/", methods=["GET"])
def ryhma(ryhma_id):
    ryhma = Ryhma.query.get_or_404(ryhma_id)

    form = LisaaJasenLomake()
    form.jasenet.choices =[(kayttaja.id, kayttaja.nimi) for kayttaja in Kayttaja.query.all()]


    return render_template("ryhmat/ryhma.html", ryhma = ryhma, form = form)

@app.route("/ryhmat/<ryhma_id>/", methods=["POST"])
def lisaa_jasenia(ryhma_id):
    
    ryhma = Ryhma.query.get_or_404(ryhma_id)
 
    form = LisaaJasenLomake(request.form)
    
    ryhma.jasenet = ryhma.jasenet + [Kayttaja.query.get(jasen_id) for jasen_id in form.jasenet.data ]
    
    db.session().commit()

    print(ryhma.jasenet)
    
    return redirect(url_for("ryhma", ryhma_id=ryhma_id))

@app.route("/ryhmat<ryhma_id>/poista", methods=["POST"])
def ryhmat_poista(ryhma_id):
    ryhma = Ryhma.query.get_or_404(ryhma_id)

    db.session.delete(ryhma)
    db.session.commit()

    return redirect(url_for("ryhmat"))
