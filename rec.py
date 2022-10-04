from flask import Blueprint, request, flash, redirect
import os
from werkzeug.utils import secure_filename
import xml.dom.minidom

rec = Blueprint("rec", __name__, static_folder="static", template_folder="templates")
path = os.getcwd()


UPLOAD_FOLDER = os.path.join(path, 'static/files')

# Receive xml file 
@rec.route("/rec_xml_file", methods = ['POST', 'GET'])
def upload_files():
    if request.method == 'POST':
        # Check if there are any files that were sent
        if 'file-input' not in request.files:
            flash("No files selected", "info")
            return redirect("/")

        # Save files into a list
        uploaded_files = request.files.getlist("file-input")
        
        # Check if directory exists and if not, then create one 
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
            
        save_type = 0
        # Function for checking if the filetype is xml 
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in "xml"
        
        # Iterate through all given files
        for file in uploaded_files:
            if allowed_file(file.filename):
                with xml.dom.minidom.parse(file) as dom:
                    # Check if it's a valid ESL file with every needed information
                    if dom.getElementsByTagName("ValueRow") and dom.getElementsByTagName("TimePeriod"):
                        row_value = dom.getElementsByTagName("ValueRow")
                        has_1_8_1 = False
                        has_1_8_2 = False
                        for r in row_value:
                            if r.getAttribute("obis") == "1-1:1.8.1":
                                has_1_8_1 = True
                            if r.getAttribute("obis") == "1-1:1.8.2":
                                has_1_8_2 = True
                        if has_1_8_1 and has_1_8_2:
                            save_type = 1
                    
                    print("Check")
                    # Check if it's a valid SDAT file with every needed information
                    if dom.getElementsByTagName("rsm:DocumentID") and dom.getElementsByTagName("rsm:Position"):
                        save_type = 2
            
                # If the file is either ESL or SDAT, then save it
                if save_type == 1 or save_type == 2:
                    flash("Uploaded some files", "info")
                    dir = ""
                    if save_type == 1:
                        dir = "/esl_files/"
                    else:
                        dir = "/sdat_files/"
                    
                    file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
        return redirect("/")
    
    flash("Please send the data via the POST method")
    return redirect("/")