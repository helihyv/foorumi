from application import app, db, login_manager
from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user
from application.viestit.models import Viesti
from application.viestit.forms import ViestiLomake, ViestinMuokkausLomake, ViestinHakuLomake
from application.aiheet.models import Aihe
from application.kayttajat.models import Kayttaja


@app.route("/viestit/uusi")
@login_required
def viestit_lomake():

    form = ViestiLomake()

    form.aiheet.choices = [(aihe.id, aihe.aihe) for aihe in Aihe.query.all()]
    form.vastattava_viesti.data = None
    return render_template("viestit/uusi.html", form=form)

@app.route("/viestit/", methods=["POST"])
@login_required
def viestit_luo():
    form = ViestiLomake(request.form)

    # choises asetettava uudelleen koska niitä ole asetettu lomakkeessa
    # tehtävä jo tässä koska automaattinen validointi tarvitsee niitä
    form.aiheet.choices = [(aihe.id, aihe.aihe) for aihe in Aihe.query.all()]

    if not form.validate():
        return render_template("viestit/uusi.html", form=form)

    aiheet = [Aihe.query.get(aihe_id) for aihe_id in form.aiheet.data]

    viesti = Viesti(form.otsikko.data, form.teksti.data, aiheet,
                    form.vastattava_viesti.data, current_user.id)
    viesti.lukeneet.append(current_user)
    db.session().add(viesti)
    db.session().commit()

    return redirect(url_for("viestit_index"))


@app.route("/viestit", methods=["GET"])
@login_required
def viestit_index():

    form = ViestinHakuLomake()

    kysely = Viesti.query

    nimi = request.args.get("nimi")

    if nimi:
        kysely = kysely.join(Viesti.kirjoittaja).filter(Kayttaja.nimi == nimi)
    
    viestit = kysely.order_by(Viesti.kirjoitusaika.desc()).all()
    return render_template("viestit/lista.html", viestit=viestit, form=form)


@app.route("/viestit/<viesti_id>")
@login_required
def viesti(viesti_id):
    viesti = Viesti.query.get_or_404(viesti_id)
    
    viesti.lukeneet.append(current_user)
    db.session.commit()
    
    vastaus_lomake = ViestiLomake()
    vastaus_lomake.aiheet.choices = [(aihe.id, aihe.aihe) for aihe in Aihe.query.all()]
    vastaus_lomake.vastattava_viesti.data = viesti_id

    muokkaus_lomake = ViestinMuokkausLomake()
    muokkaus_lomake.otsikko.data = viesti.otsikko
    muokkaus_lomake.teksti.data = viesti.teksti 

    return render_template("viestit/viesti.html", viesti=viesti, vastaus_lomake=vastaus_lomake, muokkaus_lomake=muokkaus_lomake)

@app.route("/viestit/<viesti_id>/poista", methods=["POST"])
@login_required
def viestit_poista(viesti_id):
    viesti = Viesti.query.get_or_404(viesti_id)

    if not current_user.admin:
        return login_manager.unauthorized()

    db.session.delete(viesti)
    db.session.commit()

    return redirect(url_for("viestit_index"))

@app.route("/viestit/<viesti_id>", methods=["POST"])
@login_required
def viestit_muokkaa(viesti_id):
    viesti = Viesti.query.get_or_404(viesti_id)

    if not current_user.admin:
        return login_manager.unauthorized()

    form = ViestinMuokkausLomake(request.form)

    if not form.validate():
        vastaus_lomake = ViestiLomake()
        vastaus_lomake.aiheet.choices = [(aihe.id, aihe.aihe) for aihe in Aihe.query.all()]
        vastaus_lomake.vastattava_viesti = viesti.id
        return render_template("viestit/viesti.html", viesti=viesti, vastaus_lomake=vastaus_lomake, muokkaus_lomake = form)

    viesti.otsikko = form.otsikko.data
    viesti.teksti = form.teksti.data
    viesti.muokkausaika = db.func.current_timestamp()
    db.session.commit()

    return redirect(url_for("viesti", viesti_id = viesti.id))
