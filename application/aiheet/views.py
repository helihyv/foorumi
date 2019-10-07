from application import app, db, login_manager
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application.aiheet.models import Aihe
from application.aiheet.forms import LisaaAiheLomake, MuokkaaAihettaLomake

@app.route("/aiheet",methods=["GET"])
@login_required
def aiheet():
    sivuteksti = request.args.get("sivu", 1)

    try:
        sivu = int(sivuteksti)
    except:
        sivu = 1

    return render_template("aiheet/aiheet.html", aiheet= Aihe.query.order_by(Aihe.aihe).paginate(sivu), form=LisaaAiheLomake())

@app.route("/aiheet", methods=["POST"])
@login_required
def aiheet_luo():
    form = LisaaAiheLomake(request.form)
    if not form.validate():
        return render_template("aiheet/aiheet.html", aiheet= Aihe.query.all(), form = form)

    aihe = Aihe(form.aihe.data)
    db.session.add(aihe)
    db.session.commit()

    return redirect(url_for("aiheet"))

@app.route("/aiheet/<aihe_id>/", methods=["POST"])
@login_required
def aiheet_muokkaa(aihe_id):
    aihe = Aihe.query.get_or_404(aihe_id)

    if not current_user.admin:
        return login_manager.unauthorized()

    form = MuokkaaAihettaLomake(request.form)

    if not form.validate():
        return render_template("aiheet/aihe.html", aihe = aihe, form = form)

    aihe.aihe = form.aihe.data
    db.session.commit()

    return redirect(url_for("aiheet"))

@app.route("/aiheet/<aihe_id>", methods=["GET"])
@login_required
def aihe(aihe_id):
    aihe = Aihe.query.get_or_404(aihe_id)

    form = MuokkaaAihettaLomake()
    form.aihe.data = aihe.aihe
    return render_template("aiheet/aihe.html", aihe = aihe, form = form)

@app.route("/aiheet/<aihe_id>/poista", methods=["POST"])
@login_required
def aiheet_poista(aihe_id):
    aihe = Aihe.query.get_or_404(aihe_id)

    if not current_user.admin:
        return login_manager.unauthorized()

    db.session.delete(aihe)
    db.session.commit()

    return redirect(url_for("aiheet"))
