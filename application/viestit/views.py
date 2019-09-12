from application import app, db
from flask import render_template, redirect, request, url_for
from application.viestit.models import Viesti
from application.viestit.forms import ViestiLomake
from application.aiheet.models import Aihe

@app.route("/viestit/uusi")
def viestit_lomake():

    form = ViestiLomake()

    form.aiheet.choices = [(aihe.id, aihe.aihe) for aihe in Aihe.query.all()]
    return render_template("viestit/uusi.html", form = form)

@app.route("/viestit/", methods=["POST"])
def viestit_luo():
    form = ViestiLomake(request.form)
    aiheet = [Aihe.query.get(aihe_id) for aihe_id in form.aiheet.data]


    viesti = Viesti(form.otsikko.data, form.teksti.data, aiheet)
    db.session().add(viesti)
    db.session().commit()

    print(form.aiheet.data)
    return redirect(url_for("viestit_index"))

@app.route("/viestit", methods=["GET"])
def viestit_index():
    return render_template("viestit/lista.html", viestit = Viesti.query.all())
    