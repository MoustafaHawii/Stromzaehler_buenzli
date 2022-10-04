from flask import flash
from werkzeug.utils import secure_filename
import xml.dom.minidom
from io import BytesIO

# Save uploaded xml file in the correct directory
# params: 
# uploaded_files: List of all files
# UPLOAD_FOLDER: Folder where the files will be uploaded
def save_xml(uploaded_files, UPLOAD_FOLDER) -> int:
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
                    has_2_8_1 = False
                    has_2_8_2 = False
                    for r in row_value:
                        if r.getAttribute("obis") == "1-1:1.8.1":
                            has_1_8_1 = True
                        if r.getAttribute("obis") == "1-1:1.8.2":
                            has_1_8_2 = True
                        if r.getAttribute("obis") == "1-1:2.8.1":
                            has_2_8_1 = True
                        if r.getAttribute("obis") == "1-1:2.8.2":
                            has_2_8_2 = True
                    if has_1_8_1 and has_1_8_2 and has_2_8_1 and has_2_8_2:
                        save_type = 1
                
                # Check if it's a valid SDAT file with every needed information
                if dom.getElementsByTagName("rsm:DocumentID") and dom.getElementsByTagName("rsm:Position"):
                    save_type = 2
        
            # If the file is either ESL or SDAT, then save it
            if save_type == 1 or save_type == 2:
                flash("Uploaded some files", "info")
                dir = ""
                if save_type == 1:
                    dir = "/ESL-files/"
                else:
                    dir = "/SDAT-files/"
                
                # Save file in the correct directory
                with open(UPLOAD_FOLDER + dir + secure_filename(file.filename), "wb") as f:
                    f.write(file.getbuffer())

    