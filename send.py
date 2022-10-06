from flask import Blueprint, send_file, flash, redirect
from dataHandler import reload_json_file

send = Blueprint("send", __name__, static_folder="static", template_folder="templates")

# Sends every deduplicated data to the client in a json file 
@send.route("/send_json_data", methods = ['POST', 'GET'])
def send_json_data():
    try:
        flash("Diagram updated")
        return send_file("static/files/data.json")
    except Exception as e:
	    return str(e)
 
 # Reparses the xml files and updates the json on the server
@send.route("reload_json_data")
def reload_json_data():
    flash("Starting JSON file reload...")
    reload_json_file()
    flash("JSON file reload finished")
    return redirect("/")
    