from flask import Flask, render_template
from rec import rec
from send import send

app = Flask(__name__)
app.secret_key = "apple"
app.register_blueprint(rec)
app.register_blueprint(send)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
