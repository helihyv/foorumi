from application import app, db
from flask import render_template, request, redirect, url_for
from application.aiheet.models import Aihe
from application.aiheet.forms import AiheLomake

@app.route("/aiheet",methods=["GET"])
def aiheet():
    return render_template("aiheet/aiheet.html", aiheet= Aihe.query.all(), form=AiheLomake())

@app.route("/aiheet", methods=["POST"])
def aiheet_luo():
    form = AiheLomake(request.form)
    if not form.validate():
        return render_template("aiheet/aiheet.html", aiheet= Aihe.query.all(), form = form)

    aihe = Aihe(form.aihe.data)
    db.session.add(aihe)
    db.session.commit()

    return redirect(url_for("aiheet"))

@app.route("/aiheet/<aihe_id>/", methods=["POST"])
def aiheet_muokkaa(aihe_id):
    aihe = Aihe.query.get_or_404(aihe_id)
    aihe.aihe = request.form.get("aihe")
    db.session.commit()

    return redirect(url_for("aiheet"))

@app.route("/aiheet/<aihe_id>", methods=["GET"])
def aihe(aihe_id):
    aihe = Aihe.query.get_or_404(aihe_id)

    form = AiheLomake()
    form.aihe.data = aihe.aihe
    return render_template("aiheet/aihe.html", aihe = aihe, form = form)

@app.route("/aiheet/<aihe_id>/poista", methods=["POST"])
def aiheet_poista(aihe_id):
    aihe = Aihe.query.get_or_404(aihe_id)

    db.session.delete(aihe)
    db.session.commit()

    return redirect(url_for("aiheet"))
