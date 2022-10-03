from flask import Blueprint, render_template

send = Blueprint("send", __name__, static_folder="static", template_folder="templates")

@send.route("/send")
def home():
    return render_template("index.html")