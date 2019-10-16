from application import app, db, login_manager
from flask import render_template, request, redirect, url_for
from sqlalchemy import or_
from application.ryhmat.models import Ryhma
from application.ryhmat.forms import LisaaRyhmaLomake, LisaaJasenLomake, MuutaRyhmanNimeaLomake
from application.kayttajat.models import Kayttaja
from flask_login import login_required, current_user

@app.route("/ryhmat", methods=["GET"])
@login_required
def ryhmat():

    sivuteksti = request.args.get("sivu", 1)
    try:
        sivu = int(sivuteksti)
    except:
        sivu = 1

    form = LisaaRyhmaLomake()
    form.palattava_sivu.data = sivu

    return render_template(
        "ryhmat/ryhmat.html", 
        ryhmat = Ryhma.query.order_by(Ryhma.nimi).paginate(sivu), 
        form = form
    )

@app.route("/ryhmat", methods=["POST"])
@login_required
def ryhmat_luo():
    form = LisaaRyhmaLomake(request.form)

    if not current_user.admin:
        return login_manager.unauthorized()

    if not form.validate():

        sivuteksti = form.palattava_sivu.data
        try:
            sivu = int(sivuteksti)
        except:
            sivu = 1

        return render_template(
            "ryhmat/ryhmat.html", 
            form = form,  
            ryhmat = Ryhma.query.order_by(Ryhma.nimi).paginate(sivu)
        )

    ryhma = Ryhma(form.nimi.data)
    db.session().add(ryhma)
    db.session().commit()

    return redirect(url_for("ryhma", ryhma_id=ryhma.id))

@app.route("/ryhmat/<ryhma_id>/", methods=["GET"])
@login_required
def ryhma(ryhma_id):
    ryhma = Ryhma.query.get_or_404(ryhma_id)

    lisaa_jasen_lomake = LisaaJasenLomake()
    
    lisaa_jasen_lomake.jasenet.choices = [(kayttaja.id, kayttaja.nimi) 
        for kayttaja in Kayttaja.query.filter(Kayttaja.id.notin_([(kayttaja.id) 
        for kayttaja in ryhma.jasenet 
        ])).all()]

    muokkaa_ryhmaa_lomake = MuutaRyhmanNimeaLomake()
    muokkaa_ryhmaa_lomake.nimi.data = ryhma.nimi

    return render_template(
        "ryhmat/ryhma.html", 
        ryhma = ryhma, 
        lisaa_jasen_lomake = lisaa_jasen_lomake, 
        muokkaa_ryhmaa_lomake = muokkaa_ryhmaa_lomake
    )

@app.route("/ryhmat/<ryhma_id>/jasenet", methods=["POST"])
@login_required
def lisaa_jasenia(ryhma_id):
    
    ryhma = Ryhma.query.get_or_404(ryhma_id)

    if not current_user.admin:
        return login_manager.unauthorized()
 
    form = LisaaJasenLomake(request.form)
    
    ryhma.jasenet = ryhma.jasenet + Kayttaja.query.filter(Kayttaja.id.in_(form.jasenet.data)).all(); 
    
    db.session().commit()
    
    return redirect(url_for("ryhma", ryhma_id=ryhma_id))

@app.route("/ryhmat/<ryhma_id>/jasenet/<jasen_id>/poista", methods=["POST"])
@login_required
def poista_jasenia(ryhma_id, jasen_id):

    ryhma = Ryhma.query.get_or_404(ryhma_id)
    jasen = Kayttaja.query.get_or_404(jasen_id)

    if not current_user.admin:
        return login_manager.unauthorized()

    if jasen in ryhma.jasenet:
        ryhma.jasenet.remove(jasen)
        db.session.commit()

    return redirect(url_for("ryhma", ryhma_id = ryhma.id))

@app.route("/ryhmat<ryhma_id>/poista", methods=["POST"])
@login_required

def ryhmat_poista(ryhma_id):
    ryhma = Ryhma.query.get_or_404(ryhma_id)

    if not current_user.admin:
        return login_manager.unauthorized()

    db.session.delete(ryhma)
    db.session.commit()

    return redirect(url_for("ryhmat"))

@app.route("/ryhmat/<ryhma_id>/", methods=["POST"])
@login_required
def ryhmat_muokkaa(ryhma_id):
    ryhma = Ryhma.query.get_or_404(ryhma_id)

    if not current_user.admin:
        return login_manager.unauthorized()

    form = MuutaRyhmanNimeaLomake(request.form)

    if not form.validate():
        lisaa_jasen_lomake = LisaaJasenLomake()
        lisaa_jasen_lomake.jasenet.choices =[(kayttaja.id, kayttaja.nimi) for kayttaja in Kayttaja.query.all()]

        return render_template(
            "ryhmat/ryhma.html", 
            muokkaa_ryhman_nimea_lomake = form, 
            lisaa_jasen_lomake = lisaa_jasen_lomake
        )

    ryhma.nimi = form.nimi.data

    db.session.commit()

    return redirect(url_for("ryhma", ryhma_id = ryhma.id))
