from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/display", methods = ["GET","POST"])
def display():
    return render_template("result.html")

@app.route("/graph_form", methods = ["GET","POST"])
def graph_form():
    return render_template("graph_form.html")

if __name__ == '__main__':
    app.run(debug=True)