from flask import Blueprint, render_template, request, session, url_for, redirect
from datetime import timedelta

from flask.templating import render_template_string

main = Blueprint("main", __name__, static_folder="static/main/", template_folder="templates/main/")

@main.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return render_template_string("<h1> IT WORKS </h1>")
    return render_template("signin.html")

@main.route("/home/", methods=["POST", "GET"])
def home():
    pass