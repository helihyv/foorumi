from application import app, db
from flask import render_template, request, redirect, url_for
from application.aiheet.models import Aihe

@app.route("/aiheet",methods=["GET"])
def aiheet():
    return render_template("aiheet/aiheet.html", aiheet= Aihe.query.all())

@app.route("/aiheet", methods=["POST"])
def aiheet_luo():
    aihe = Aihe(request.form.get("aihe"))
    db.session.add(aihe)
    db.session().commit()

    return redirect(url_for("aiheet"))

@app.route("/aiheet/<aihe_id>/", methods=["POST"])
def aiheet_muokkaa(aihe_id):
    aihe = Aihe.query.get(aihe_id)
    aihe.aihe = request.form.get("aihe")
    db.session.commit()

    return redirect(url_for("aiheet"))