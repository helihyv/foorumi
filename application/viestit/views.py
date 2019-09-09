from application import app, db
from flask import render_template, redirect, request, url_for
from application.viestit.models import Viesti

@app.route("/viestit/uusi")
def viestit_lomake():
    return render_template("viestit/uusi.html")

@app.route("/viestit/", methods=["POST"])
def viestit_luo():
    viesti = Viesti(request.form.get("otsikko"),request.form.get("teksti"))
    db.session().add(viesti)
    db.session().commit()
    print(request.form.get("otsikko"))
    print(request.form.get("teksti"))

    return redirect(url_for("viestit_index"))

@app.route("/viestit", methods=["GET"])
def viestit_index():
    return render_template("viestit/lista.html", viestit = Viesti.query.all())
    