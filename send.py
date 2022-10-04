from flask import Blueprint, jsonify, flash

send = Blueprint("send", __name__, static_folder="static", template_folder="templates")

# Sends every deduplicated data to the client in a json file 
@send.route('/send_json_data', methods = ['POST', 'GET'])
def send_json_data():
    
    return jsonify({
        "sensorId": "ID742",
        "data": {
        "ts": "2022-09-02T07:31:06Z",
        "feedR": "1.2",
        "usgR": "3",
        "feedA": "2999",
        "usgA": "2000"
    }})