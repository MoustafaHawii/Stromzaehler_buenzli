from flask import Blueprint, request
import os
import werkzeug

rec = Blueprint("rec", __name__, static_folder="static", template_folder="templates")

# Receive xml file 
@rec.route("/rec_xml_file", methods = ['POST', 'GET'])
def rec_files():
    if request.method == 'POST':
      uploaded_files = request.files.getlist("file[]")
      for file in uploaded_files:
        file.save(os.path.join(rec.config("UPLOAD_FOLDER")), werkzeug.secure_filename(file.filename))
      return 'file uploaded successfully'
    return "No file selected or false method was used"