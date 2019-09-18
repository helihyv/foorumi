from application import app, db
from flask import render_template
from flask_login import login_required

@app.route("/tilastot")
@login_required
def tilastot():
    return render_template("tilastot/tilastot.html")