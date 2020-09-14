from flask import Blueprint, render_template, request, session, url_for, redirect
from datetime import timedelta

main = Blueprint("main", __name__, static_folder="static/main/", template_folder="templates/main/")

@main.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("home"))
    else:
        if "user" in session:
            return redirect(url_for("home"))

        return render_template("signin.html")
    return render_template("signin.html")


@main.route("/home", methods=["POST", "GET"])
def home():
    pass