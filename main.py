from flask import Blueprint, render_template, request, url_for, redirect, flash, make_response
from datetime import datetime, timedelta
from flask.templating import render_template_string

import authenticate

main = Blueprint("main", __name__, static_folder="static/main/", template_folder="templates/main/")

@main.route("/", methods=["POST", "GET"])
def login():
    # Check to see if cookie is in or not
    if 'Exist' in request.cookies and 'DistrictCode' in request.cookies:
        return redirect(url_for('main.dashboard'))

    # Validation of Login
    elif request.method == "POST":
        Values = authenticate.Login(request.form['DistrictCode'], request.form['Username'], request.form['Password'])
        if Values == -1:
            flash("Username, or Password is incorrect.", category="error")
            return redirect(url_for("main.login"))
        elif Values == -2:
            flash("Network Error/Wrong District Code. Please try again.", category="error")
            return redirect(url_for("main.login"))
        else:
            # Don't touch it please
            expire_date = datetime.now()
            expire_date += timedelta(days=360)

            res = make_response(url_for('main.dashboard'), 200)

            # Set secure to true to deployment
            res.set_cookie("Exist", '1', expires=expire_date, secure=False)
            res.set_cookie("DistrictCode", Values[0], expires=expire_date, secure=False)
            res.set_cookie("Username", Values[1], expires=expire_date, secure=False)
            res.set_cookie("Password", Values[2], expires=expire_date, secure=False)

            return res
    else:
        # If not a post request then show signin page
        return render_template("signin.html")



@main.route("/dashboard/", methods=["GET"])
def dashboard():
    cookies = request.cookies
    if 'Exist' in cookies:
        DistrictCode = cookies.get('DistrictCode')
        Username = cookies.get('Username')
        Password = cookies.get('Password')
        return render_template_string(f"{DistrictCode} {Username} {Password}")
    
    else:
        return redirect(url_for('main.login'))
