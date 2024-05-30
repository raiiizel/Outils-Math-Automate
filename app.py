from flask import Flask, request
from flask import render_template
from Automate.automate_application_phase import *
from Automate.automate_render import *
app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/display", methods = ["GET","POST"])
def display():
    graph_type_dict = {
        "simple":TypeGraphe.Simple,
        "complet": TypeGraphe.Complet,
        "eulerien": TypeGraphe.Eulerien,
        "complet_biparti": TypeGraphe.CompletBipartis,
        "hamiltonien": TypeGraphe.Hamiltonien
        }

    if request.method == "POST":
        nb_neouds = request.form.get("nb_noeuds")
        print(nb_neouds)
        dirige_ou_non = int(request.form["dirige_ou_non"]) #String 0 is equel to true when converted directly to bool
        value_ou_non = int(request.form["value_ou_non"])
        type_graphe = request.form["type_graphe"]
        #TODO: generate the graphe and automaton and pass the files' urls to the template
        
        automaton_image_url="static/automaton.png"
        graphe_image_url="static/graphe.png"

    return render_template("result.html",automaton_image_url=automaton_image_url,  graphe_image_url=graphe_image_url)

@app.route("/graph_form", methods = ["GET","POST"])
def graph_form():
    return render_template("graph_form.html")

if __name__ == '__main__':
    app.run(debug=True)