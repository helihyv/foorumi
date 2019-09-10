from application import app, db
from flask import render_template

@app.route("/tilastot")
def tilastot():
    return render_template("tilastot/tilastot.html")