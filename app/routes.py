from flask import (
    Flask,
    render_template,
    request
    )
from datetime import datetime
import requests

app = Flask (__name__)

BASE_URL = "http://127.0.0.1:5000/cars"


@app.get('/')
def main():
    timestamp = datetime.now().strftime("%F %H:%M:%S")
    return render_template('home.html', ts=timestamp)


@app.get("/about")
def about_page():
    return render_template("about.html")


@app.get("/cars")
def display_all_cars():
    resp = requests.get(BASE_URL)
    if resp.status_code == 200:
        car_list = resp.json().get("cars")
        return render_template("list.html", cars=car_list)
    return render_template("error.html", err=resp.status_code), resp.status_code

@app.get("/cars/<int:pk>")
def display_car(pk):
    url = "%s/%s" % (BASE_URL, pk)
    resp = requests.get(url)
    if resp.status_code == 200:
        car = resp.json().get("car")
        return render_template("detail.html", car=car)
    return render_template("error.html", err=resp.status_code), resp.status_code


@app.get("/cars/new")
def new_car_form():
    return render_template("new.html")


@app.post("/cars/new")
def create_car():
    car_data = request.form
    car_json = {
        "type_car": car_data.get("type_car"),
        "color":  car_data.get("color"),
        "license": car_data.get("license"),
        "owner_last_name": car_data.get("owner_last_name"),
        "owner_first_name": car_data.get("owner_first_name")
    }
    resp = requests.post(BASE_URL, json=car_json)
    if resp.status_code == 204:
        return render_template("success.html", success=True)
    return render_template("error.html", success=True), resp.status_code

@app.route("/cars/<int:pk>", methods=['DELETE'])
def delete_car(pk):
    print("Eliminando")
    url = "%s/%s" % (BASE_URL, pk)
    resp = requests.delete(url)
    if resp.status_code == 204:
        return render_template("success.html", success=True)
    return render_template("error.html", success=True), resp.status_code
