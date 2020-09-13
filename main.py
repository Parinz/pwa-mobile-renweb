from flask import Blueprint, render_template

main = Blueprint("main", __name__, static_folder="static/main/", template_folder="templates/main/")

@main.route("/")
def home():
    return render_template("signin.html")