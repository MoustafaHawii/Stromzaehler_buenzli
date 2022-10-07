from flask import Blueprint, request, flash, redirect
import os
from dataHandler import save_xml

rec = Blueprint("rec", __name__, static_folder="static", template_folder="templates")
path = os.getcwd()

# folder where sdat and esl files are stored
UPLOAD_FOLDER = os.path.join(path, 'static/files')

# Receive xml file 
@rec.route("/rec_xml_file", methods = ['POST', 'GET'])
def upload_files():
    print("HI")
    if request.method == 'POST':
        # Check if there are any files that were sent
        if 'file-input' not in request.files:
            flash("No files selected", "info")
            return redirect("/")

        # Save files into a list
        uploaded_files = request.files.getlist("file-input")
        save_xml(uploaded_files, UPLOAD_FOLDER)
        return redirect("/")
    
    flash("Please send the data via the POST method", "info")
    return redirect("/")

