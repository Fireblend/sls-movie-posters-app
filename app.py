import os
import json
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

API_KEY = os.environ['API_KEY']
BASE_URL = os.environ['API_BASE_URL']

default_name = "Kiki's Delivery Service"
default_data = {"poster": "https://www.themoviedb.org/t/p/w500//7nO5DUMnGUuXrA4r2h6ESOKQRrx.jpg", "primaryColor": "#6BA2D5", "otherColors": [{"color": "#2B4282", "proportion": 0.41303306181121224}, {"color": "#96C0E5", "proportion": 0.16626736942980355}, {"color": "#C8D5E2", "proportion": 0.15572592237661714}, {"color": "#607291", "proportion": 0.1317680881648299}, {"color": "#2E2A31", "proportion": 0.06851940584571155}, {"color": "#BAAC93", "proportion": 0.06468615237182558}]}

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
