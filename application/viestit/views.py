from application import app, db, login_manager
from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user
from datetime import time, datetime
from application.viestit.models import Viesti
from application.viestit.forms import ViestiLomake, ViestinMuokkausLomake, ViestinHakuLomake
from application.aiheet.models import Aihe
from application.kayttajat.models import Kayttaja
from application.ryhmat.models import Ryhma


@app.route("/viestit/uusi")
@login_required
def viestit_lomake():

    form = ViestiLomake()

    form.aiheet.choices = [(aihe.id, aihe.aihe) for aihe in Aihe.query.order_by(Aihe.aihe).all()]
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

    kysely = Viesti.query

    # Hakuehdoista aiheen, kirjoittajan ja ryhmän pituutta ei validoida, 
    # koska satojakaan merkkejä pitkä hakuehto ei tuota ongelmia palvelimelle

    aihe = request.args.get("aihe")

    hakuparametrit = "&"

    virheet = []
    if aihe:
        kysely = kysely.join(Viesti.aiheet).filter(Aihe.aihe == aihe)
        hakuparametrit = hakuparametrit + "aihe=" + aihe + "&"


    nimi = request.args.get("nimi")

    ryhma = request.args.get("ryhma")

    if nimi or ryhma:
        kysely = kysely.join(Viesti.kirjoittaja)

    if nimi:
        kysely = kysely.filter(Kayttaja.nimi == nimi)
        hakuparametrit = hakuparametrit + "nimi=" + nimi + "&"


    if ryhma:
        kysely = kysely.join(Kayttaja.kayttajat).filter(Ryhma.nimi == ryhma)
        hakuparametrit = hakuparametrit + "ryhma=" + ryhma + "&"

    alkupvm = request.args.get("alkupvm")
    
    #Varmistetaan, että syöte on validi päivämäärä
    #Päivämäärä validoidaan jo asiakkaan puolella, ei tarvetta virheilmoitukselle
    try:
        alkupvm = datetime.strptime(alkupvm, "%Y-%m-%d")
    except:
        alkupvm = None

    else:
        kysely = kysely.filter(Viesti.kirjoitusaika >= alkupvm)
        hakuparametrit = hakuparametrit + "alkupvm=" + str(alkupvm) + "&"            

    loppupvm = request.args.get("loppupvm")
    
    #Varmistetaan, että syöte on validi päivämäärä
    #Päivämäärä validoidaan jo asiakkaan puolella, ei tarvetta virheilmoitukselle
    try:
        loppupvm = datetime.strptime(loppupvm,"%Y-%m-%d")
    except:
        loppupvm=None
    else:
        kysely = kysely.filter(Viesti.kirjoitusaika <= str(loppupvm) + " " +  str(time(23,59,59,999999))) 
        hakuparametrit = hakuparametrit + "loppupvm=" + str(loppupvm)

    sivuteksti = request.args.get("sivu", 1)
    try:
        sivu = int(sivuteksti)
    except:
        sivu = 1
    
    viestit = kysely.order_by(Viesti.kirjoitusaika.desc()).paginate(sivu)

    form = ViestinHakuLomake()

    return render_template(
        "viestit/lista.html", 
        viestit=viestit, 
        form=form, haettu_aihe=aihe, 
        haettu_kirjoittaja=nimi, 
        haettu_ryhma = ryhma, 
        haettu_aika_alku = alkupvm, 
        haettu_aika_loppu = loppupvm, 
        hakuparametrit=hakuparametrit, 
        virheet = virheet
        )


@app.route("/viestit/<viesti_id>")
@login_required
def viesti(viesti_id):
    viesti = Viesti.query.get_or_404(viesti_id)
    vastaus_lomake = ViestiLomake()
    vastaus_lomake.aiheet.choices = [
        (aihe.id, aihe.aihe) for aihe in Aihe.query.order_by(Aihe.aihe).all()]
    vastaus_lomake.vastattava_viesti.data = viesti_id
    muokkaus_lomake = ViestinMuokkausLomake()
    muokkaus_lomake.otsikko.data = viesti.otsikko
    muokkaus_lomake.teksti.data = viesti.teksti

    if not viesti.onko_lukenut(current_user):
        viesti.lukeneet.append(current_user)
        db.session.commit()

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

    return redirect(url_for("viesti", viesti_id = viesti_id))
