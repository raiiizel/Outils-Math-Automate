from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/display", methods = ["GET","POST"])
def display():
    return render_template("result.html")


if __name__ == '__main__':
    app.run(debug=True)