from application import app, db
from flask import render_template

@app.route("/ryhmat")
def ryhmat():
    return render_template("ryhmat/ryhmat.html")
