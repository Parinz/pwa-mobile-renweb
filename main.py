from flask import Blueprint, render_template, request, session, url_for, redirect
from datetime import timedelta
from flask.templating import render_template_string

import authenticate

main = Blueprint("main", __name__, static_folder="static/main/", template_folder="templates/main/")

@main.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        Values = authenticate.Login(request.form['DistrictCode'], request.form['Username'], request.form['Password'])
        if Values == -1:
            return render_template_string("Wrong Pass")
        else:
            return render_template_string(f"Functioning Properly {Values[0]} {Values[1]} {Values[2]}")
    else:
        return render_template("signin.html")

@main.route("/cookies", methods=["GET"])
def cookies():
    return render_template_string("<h1> IT WORKS </h1>")

@main.route("/home/", methods=["POST", "GET"])
def home():
    pass