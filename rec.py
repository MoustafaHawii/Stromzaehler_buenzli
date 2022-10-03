from flask import Blueprint, render_template

rec = Blueprint("rec", __name__, static_folder="static", template_folder="templates")

@rec.route("/rec")
def hello():
    return render_template("index.html")