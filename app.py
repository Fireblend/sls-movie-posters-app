import os
import json
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

API_KEY = os.environ['API_KEY']
BASE_URL = os.environ['API_BASE_URL']

default_name = "Kiki's Delivery Service"
default_data = {"poster": "https://www.themoviedb.org/t/p/w500//7nO5DUMnGUuXrA4r2h6ESOKQRrx.jpg", "primaryColor": "#66A1D7", "otherColors": [{"color": "#293E7B", "proportion": 0.31275349256421814}, {"color": "#C5D5E5", "proportion": 0.16223524109959442}, {"color": "#8BB9E2", "proportion": 0.15998197386210006}, {"color": "#365291", "proportion": 0.08877872915727805}, {"color": "#5B78A2", "proportion": 0.08021631365479946}, {"color": "#95A3B4", "proportion": 0.07300585849481749}, {"color": "#26242A", "proportion": 0.05497972059486255}, {"color": "#736261", "proportion": 0.03830554303740424}, {"color": "#BFA47C", "proportion": 0.029743127534925643}]}

@app.route("/")
def index():
    return render_template("index.html", data=default_data, name=default_name)

@app.route("/", methods=['POST'])
def result():

    query = request.form["query"]
    result = requests.get(f"{BASE_URL}/prod/movie?query={query}", 
             headers={"x-api-key":API_KEY}).text

    if "primaryColor" in result:
        return render_template("index.html", data=json.loads(result), name=query)
    else:
        return render_template("index.html", data=default_data, name="Movie Not Found!")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
