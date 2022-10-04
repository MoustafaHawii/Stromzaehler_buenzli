from flask import Flask, render_template
from rec import rec
from send import send
import uuid

app = Flask(__name__)
SECRET_KEY = uuid.uuid4().hex
app.secret_key = SECRET_KEY
app.config["SECRET_KEY"] = SECRET_KEY

app.register_blueprint(rec)
app.register_blueprint(send)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
  app.run(debug=True)