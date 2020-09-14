from flask import Flask, render_template, url_for, flash, redirect, request
from main import main


app = Flask(__name__)
app.register_blueprint(main, url_prefix="/app/")
app.secret_key = "oppwiZtFNM5UOH011tqISvDoi8L5ehxFFsReI1iebD2DrY1wha--ZwVIf0Z47uuTovGlXr7bHDjsmOUGVaFCqWR7zBiAuZymRdP0_cNk10X26J6skfTZI1bh1shJUdvK7fisKg"


##### DEFUALT TO HTTPS ENABLE ON PRODUCTION

# @app.before_request
# def before_request():
#     if request.url.startswith("http://"):
#         url = request.url.replace("http://", "https://", 1)
#         code = 301
#         return redirect(url, code=code)


###### Show Pages

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/guide")
def guide():
    return render_template("guide.html")


