from application import app, db
from flask import render_template
from flask_login import login_required

@app.route("/ryhmat")
@login_required
def ryhmat():
    return render_template("ryhmat/ryhmat.html")
