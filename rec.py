from flask import Blueprint, request, flash, redirect
import os
from werkzeug.utils import secure_filename

rec = Blueprint("rec", __name__, static_folder="static", template_folder="templates")
path = os.getcwd()


UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Receive xml file 
@rec.route("/rec_xml_file", methods = ['POST', 'GET'])
def upload_files():
    if request.method == 'POST':
        if 'file-input' not in request.files:
            flash('No file part')
            return "No file sent"
            #return redirect(request.url)
        # Function for checking if the filename contains xml 
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in "xml"

        # Save files into a list
        uploaded_files = request.files.getlist("file-input")
        for f in uploaded_files:
            print(f.filename)
        
        # Check if directory exists and if not, then create one 
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        # Save files if the file has .xml type
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))

        flash('File(s) successfully uploaded')
        return redirect("/")
    return "No file selected or false method was used"